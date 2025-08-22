#!/usr/bin/env python3
"""
ftp_upload.py

Recursively upload a local directory (default: `api`) to a remote FTP server using the
configuration in `.vscode/ftp-sync.json` by default.

Usage:
  python3 scripts/ftp_upload.py [--local LOCAL_DIR] [--config CONFIG_JSON] [--remote REMOTE_PATH] [--dry-run]

The script will:
 - Read FTP connection settings from the config file (or environment variables)
 - Connect to the FTP server (supports FTP and FTPS based on config)
 - Create remote directories as needed
 - Upload files with binary mode
 - Log errors to `errors.txt` in repo root if anything fails

Note: Credentials in `.vscode/ftp-sync.json` are used if present. You can override
with environment variables: FTP_HOST, FTP_USER, FTP_PASS, FTP_PORT, FTP_REMOTE.
"""

import argparse
import json
import os
import ftplib
import sys
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / '.vscode' / 'ftp-sync.json'
ERRORS_FILE = ROOT / 'errors.txt'


def read_config(path: Path):
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read config {path}: {e}")


def make_remote_dirs(ftp: ftplib.FTP, remote_path: str):
    # create and cd into each component
    parts = [p for p in remote_path.replace('\\', '/').split('/') if p and p not in ('.', '')]
    for part in parts:
        try:
            ftp.cwd(part)
        except Exception:
            try:
                ftp.mkd(part)
                ftp.cwd(part)
            except Exception as e:
                raise RuntimeError(f"Failed to create/enter remote dir '{part}': {e}")


def upload_directory(ftp: ftplib.FTP, local_base: Path, remote_base: str, dry_run: bool = False):
    errors = []
    # Normalize remote base
    if remote_base.startswith('./'):
        remote_base = remote_base[2:]

    for root, dirs, files in os.walk(local_base):
        rel = os.path.relpath(root, local_base)
        if rel == '.' or rel == './':
            remote_dir = remote_base
        else:
            remote_dir = '/'.join([remote_base, rel]).strip('/')

        try:
            ftp.cwd('/')
            if remote_dir:
                make_remote_dirs(ftp, remote_dir)
        except Exception as e:
            errors.append(f"Could not prepare remote dir {remote_dir}: {e}")
            continue

        for fname in files:
            local_path = Path(root) / fname
            if dry_run:
                print(f"DRY RUN: would upload {local_path} -> {remote_dir}/{fname}")
                continue

            try:
                with open(local_path, 'rb') as f:
                    ftp.storbinary(f'STOR {fname}', f)
                print(f"Uploaded {local_path} -> {remote_dir}/{fname}")
            except Exception as e:
                errors.append(f"Failed to upload {local_path} -> {remote_dir}/{fname}: {e}")

    return errors


def upload_file(ftp: ftplib.FTP, local_base: Path, local_path: Path, remote_base: str, dry_run: bool = False):
    """Upload a single file keeping the same relative path under remote_base."""
    rel = os.path.relpath(str(local_path), str(local_base))
    # remote dir = remote_base + dirname(rel)
    dirname = os.path.dirname(rel)
    if dirname == '.' or dirname == './':
        remote_dir = remote_base
    else:
        remote_dir = '/'.join([remote_base, dirname]).strip('/')

    if dry_run:
        print(f"DRY RUN: would upload {local_path} -> {remote_dir}/{local_path.name}")
        return None

    try:
        ftp.cwd('/')
        if remote_dir:
            make_remote_dirs(ftp, remote_dir)
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {local_path.name}', f)
        print(f"Uploaded {local_path} -> {remote_dir}/{local_path.name}")
        return None
    except Exception as e:
        return f"Failed to upload {local_path} -> {remote_dir}/{local_path.name}: {e}"


def build_local_state(local_base: Path):
    state = {}
    for root, dirs, files in os.walk(local_base):
        for fname in files:
            p = Path(root) / fname
            try:
                state[str(p)] = p.stat().st_mtime
            except Exception:
                state[str(p)] = 0
    return state


def watch_and_upload(connect_info, local_base: Path, remote_base: str, dry_run: bool = False, poll_interval: float = 1.5):
    host, port, user, passwd, passive, secure = connect_info

    # Build initial state
    prev_state = build_local_state(local_base)

    # Create ftp connection
    def make_ftp():
        if secure:
            ftp = ftplib.FTP_TLS()
        else:
            ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=30)
        ftp.login(user, passwd)
        ftp.set_pasv(passive)
        return ftp

    ftp = None
    try:
        ftp = make_ftp()
    except Exception as e:
        print('Failed to connect for watch mode:', e)
        return [str(e)]

    errors = []
    print('Watching', local_base, 'for changes. Press Ctrl-C to stop.')
    try:
        while True:
            time.sleep(poll_interval)
            try:
                current = build_local_state(local_base)
            except Exception as e:
                errors.append(str(e))
                continue

            # detect new or modified files
            changed = []
            for path, mtime in current.items():
                if path not in prev_state or prev_state[path] < mtime:
                    changed.append(path)

            # update prev_state for files removed
            prev_state = current.copy()

            for p in changed:
                local_path = Path(p)
                # attempt upload, with reconnect on failure
                try:
                    err = upload_file(ftp, local_base, local_path, remote_base, dry_run=dry_run)
                    if err:
                        # try reconnect once
                        try:
                            ftp.close()
                        except Exception:
                            pass
                        try:
                            ftp = make_ftp()
                            err = upload_file(ftp, local_base, local_path, remote_base, dry_run=dry_run)
                        except Exception as e:
                            err = f"Reconnect + upload failed for {local_path}: {e}"

                    if err:
                        print(err)
                        errors.append(err)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    err = f"Unhandled error uploading {local_path}: {e}"
                    print(err)
                    errors.append(err)

    except KeyboardInterrupt:
        print('\nWatcher stopped by user')
    finally:
        try:
            if ftp:
                ftp.quit()
        except Exception:
            pass

    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', '-l', default='api', help='Local directory to upload (default: api)')
    parser.add_argument('--config', '-c', default=str(DEFAULT_CONFIG), help='Path to ftp config JSON')
    parser.add_argument('--remote', '-r', help='Remote base path (overrides config remotePath)')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without uploading')
    parser.add_argument('--watch', '-w', action='store_true', help='Watch local dir and upload changed files')
    args = parser.parse_args()

    cfg = read_config(Path(args.config))

    host = os.environ.get('FTP_HOST') or cfg.get('host')
    user = os.environ.get('FTP_USER') or cfg.get('username')
    passwd = os.environ.get('FTP_PASS') or cfg.get('password')
    port = int(os.environ.get('FTP_PORT') or cfg.get('port', 21))
    remote_base = args.remote or os.environ.get('FTP_REMOTE') or cfg.get('remotePath', './')
    passive = cfg.get('passive', True)
    secure = cfg.get('secure', False)

    if not host or not user or not passwd:
        print('Missing FTP credentials. Provide them in the config or set FTP_HOST/FTP_USER/FTP_PASS env vars.')
        sys.exit(2)

    local_base = Path(args.local)
    if not local_base.exists() or not local_base.is_dir():
        print(f'Local directory not found: {local_base}')
        sys.exit(2)

    ftp = None
    errors = []
    try:
        if secure:
            ftp = ftplib.FTP_TLS()
        else:
            ftp = ftplib.FTP()

        ftp.connect(host, port, timeout=30)
        ftp.login(user, passwd)
        ftp.set_pasv(passive)

        if args.watch:
            # close initial connection; watch_and_upload will create its own connection handling
            try:
                ftp.quit()
            except Exception:
                pass
            connect_info = (host, port, user, passwd, passive, secure)
            errors = watch_and_upload(connect_info, local_base, remote_base, dry_run=args.dry_run)
        else:
            uploaded_errors = upload_directory(ftp, local_base, remote_base, dry_run=args.dry_run)
            errors.extend(uploaded_errors)

        try:
            ftp.quit()
        except Exception:
            pass

    except Exception as e:
        errors.append(str(e))

    if errors:
        with open(ERRORS_FILE, 'a', encoding='utf-8') as ef:
            for err in errors:
                ef.write(err + '\n')
        print('Completed with errors; see errors.txt')
        sys.exit(1)

    print('Upload completed successfully')


if __name__ == '__main__':
    main()
