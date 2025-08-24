#!/usr/bin/env python3
"""
onsave_sync.py

Watch for file save/edit events under the project and upload changed files
using the FTPUploader class from scripts/ftp_upload.py.

This script uses the watchdog library if available for efficient file system
event monitoring, otherwise falls back to polling. It respects the allow/ignore
patterns from ftp-sync.json configuration.

Usage:
  python3 scripts/onsave_sync.py [--local LOCAL_DIR] [--config CONFIG_JSON] [--remote REMOTE_PATH] [--dry-run]

The script validates FTP credentials (env vars or config) before starting.
"""

import sys
import time
import os
import argparse
from pathlib import Path
import logging
import fnmatch
import ftplib

ROOT = Path(__file__).resolve().parents[1]
FTP_UPLOAD_PATH = ROOT / 'scripts' / 'ftp_upload.py'
LOG_FILE = ROOT / 'onsave_sync.log'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_ftp_uploader():
    """Import and return the FTPUploader class from ftp_upload.py"""
    import importlib.util
    
    if not FTP_UPLOAD_PATH.exists():
        raise RuntimeError(f'Required script not found: {FTP_UPLOAD_PATH}')
    
    spec = importlib.util.spec_from_file_location('ftp_upload', str(FTP_UPLOAD_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.FTPUploader, getattr(module, 'DEFAULT_EXCLUDES', [])


class FileWatcher:
    """File watcher that monitors changes and uploads files"""
    
    def __init__(self, uploader, local_base: Path, remote_base: str, default_excludes: list, dry_run: bool = False):
        self.uploader = uploader
        self.local_base = local_base.resolve()
        self.remote_base = remote_base
        self.default_excludes = default_excludes
        self.dry_run = dry_run
        self.last_upload_times = {}  # Track last upload time to avoid duplicate uploads
        self.known_files = set()  # Track known files for deletion detection
    
    def should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed (not excluded and within base directory)"""
        try:
            file_path = file_path.resolve()
            
            # Must be under local_base
            if not str(file_path).startswith(str(self.local_base)):
                return False
            
            # Don't process log files to avoid loops
            if file_path.name.endswith('.log'):
                return False
            
            # Don't process if it's our own log file
            if file_path == LOG_FILE.resolve():
                return False
            
            # Check against allow/ignore patterns early
            rel_path = os.path.relpath(file_path, self.local_base)
            allows = self.uploader.config.get('allow', [])
            ignores = self.uploader.config.get('ignore', []) + self.default_excludes
            
            def matches_patterns(path: str, patterns: list) -> bool:
                for pattern in patterns:
                    # Handle escaped dots in JSON
                    try_patterns = [pattern, pattern.replace('\\.', '.')]
                    for tp in try_patterns:
                        if fnmatch.fnmatch(path, tp) or fnmatch.fnmatch(os.path.basename(path), tp):
                            return True
                return False
            
            # If allow patterns exist, file must match at least one
            if allows:
                if not matches_patterns(rel_path, allows):
                    return False
            
            # Check ignore patterns
            if matches_patterns(rel_path, ignores):
                return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking file {file_path}: {e}")
            return False
    
    def upload_file(self, file_path: Path):
        """Upload a single file with duplicate prevention"""
        if not self.should_process_file(file_path):
            logger.debug(f"SKIP (filtered): {file_path}")
            return
        
        try:
            # Get file modification time to prevent duplicate uploads
            mtime = file_path.stat().st_mtime
            file_key = str(file_path)
            
            # Skip if we recently uploaded this file
            if file_key in self.last_upload_times:
                if mtime <= self.last_upload_times[file_key]:
                    return
            
            logger.info(f"Detected change: {file_path}")
            
            if self.dry_run:
                logger.info(f"DRY RUN: would upload {file_path}")
                return
            
            # Upload the file
            error = self.uploader.upload_file(file_path, self.remote_base, self.local_base, self.dry_run)
            
            if error:
                logger.error(f"Upload failed: {error}")
                # Try reconnecting once
                try:
                    self.uploader.disconnect()
                    error = self.uploader.upload_file(file_path, self.remote_base, self.local_base, self.dry_run)
                    if error:
                        logger.error(f"Upload failed after reconnect: {error}")
                    else:
                        logger.info(f"Upload successful after reconnect: {file_path}")
                        self.last_upload_times[file_key] = mtime
                except Exception as e:
                    logger.error(f"Reconnection failed: {e}")
            else:
                logger.info(f"Upload successful: {file_path}")
                self.last_upload_times[file_key] = mtime
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")


    def delete_remote_file(self, local_file_path: Path):
        """Delete a file from the remote server"""
        try:
            # Calculate relative path and remote path
            rel_path = os.path.relpath(local_file_path, self.local_base)
            
            # Calculate remote file path
            rel_dir = os.path.dirname(rel_path)
            if rel_dir and rel_dir != '.':
                remote_dir = f"{self.remote_base.strip('/')}/{rel_dir}".strip('/')
            else:
                remote_dir = self.remote_base.strip('/')
            
            remote_file_path = f"{remote_dir}/{local_file_path.name}" if remote_dir else local_file_path.name
            
            if self.dry_run:
                logger.info(f"DRY RUN: would delete {remote_file_path}")
                return
            
            # Connect if not already connected
            if not self.uploader.ftp:
                self.uploader.ftp = self.uploader.connect()
            
            # Navigate to the remote directory
            self.uploader.ftp.cwd('/')
            if remote_dir:
                try:
                    self.uploader.ftp.cwd(remote_dir)
                except ftplib.error_perm:
                    logger.warning(f"Remote directory not found for deletion: {remote_dir}")
                    return
            
            # Delete the file
            try:
                self.uploader.ftp.delete(local_file_path.name)
                logger.info(f"Deleted remote file: {remote_file_path}")
            except ftplib.error_perm as e:
                if '550' in str(e):  # File not found
                    logger.info(f"Remote file already deleted: {remote_file_path}")
                else:
                    logger.error(f"Failed to delete remote file {remote_file_path}: {e}")
            
        except Exception as e:
            logger.error(f"Error deleting remote file for {local_file_path}: {e}")


def run_watchdog_watcher(watcher: FileWatcher):
    """Use watchdog for efficient file system monitoring"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        raise ImportError("watchdog library not available")
    
    class FileChangeHandler(FileSystemEventHandler):
        def __init__(self, watcher):
            self.watcher = watcher
            super().__init__()
        
        def on_modified(self, event):
            if not event.is_directory:
                self.watcher.upload_file(Path(event.src_path))
        
        def on_created(self, event):
            if not event.is_directory:
                file_path = Path(event.src_path)
                self.watcher.known_files.add(file_path)
                self.watcher.upload_file(file_path)
        
        def on_moved(self, event):
            if not event.is_directory:
                # Handle move as delete old + create new
                old_path = Path(event.src_path)
                new_path = Path(event.dest_path)
                
                if old_path in self.watcher.known_files:
                    self.watcher.known_files.remove(old_path)
                    if self.watcher.should_process_file(old_path):
                        logger.info(f"Detected file move (delete): {old_path}")
                        self.watcher.delete_remote_file(old_path)
                
                self.watcher.known_files.add(new_path)
                self.watcher.upload_file(new_path)
        
        def on_deleted(self, event):
            if not event.is_directory:
                file_path = Path(event.src_path)
                if file_path in self.watcher.known_files:
                    self.watcher.known_files.remove(file_path)
                    if self.watcher.should_process_file(file_path):
                        logger.info(f"Detected file deletion: {file_path}")
                        self.watcher.delete_remote_file(file_path)
    
    observer = Observer()
    handler = FileChangeHandler(watcher)
    
    # Initialize known files set
    watcher.known_files = watcher.scan_files()
    logger.info(f"Tracking {len(watcher.known_files)} files for changes and deletions")
    
    observer.schedule(handler, str(watcher.local_base), recursive=True)
    
    observer.start()
    logger.info(f"Watching {watcher.local_base} for changes using watchdog. Press Ctrl-C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")
    finally:
        observer.stop()
        observer.join()


def run_polling_watcher(watcher: FileWatcher, poll_interval: float = 1.5):
    """Fallback polling-based file watcher"""
    logger.info(f"Watching {watcher.local_base} for changes using polling. Press Ctrl-C to stop.")
    
    # Build initial file state
    file_mtimes = {}
    
    def scan_files():
        current_files = {}
        try:
            for root, dirs, files in os.walk(watcher.local_base):
                for filename in files:
                    file_path = Path(root) / filename
                    if watcher.should_process_file(file_path):
                        try:
                            current_files[str(file_path)] = file_path.stat().st_mtime
                        except Exception:
                            current_files[str(file_path)] = 0
        except Exception as e:
            logger.error(f"Error scanning files: {e}")
        return current_files
    
    file_mtimes = scan_files()
    watcher.known_files = {Path(f) for f in file_mtimes.keys()}
    logger.info(f"Tracking {len(watcher.known_files)} files for changes and deletions")
    
    try:
        while True:
            time.sleep(poll_interval)
            
            current_files = scan_files()
            current_paths = set(current_files.keys())
            previous_paths = set(file_mtimes.keys())
            
            # Check for new or modified files
            for file_path_str, mtime in current_files.items():
                if file_path_str not in file_mtimes or file_mtimes[file_path_str] < mtime:
                    file_path = Path(file_path_str)
                    watcher.known_files.add(file_path)
                    watcher.upload_file(file_path)
            
            # Check for deleted files
            deleted_files = previous_paths - current_paths
            for deleted_file_str in deleted_files:
                deleted_file = Path(deleted_file_str)
                if deleted_file in watcher.known_files:
                    watcher.known_files.remove(deleted_file)
                    logger.info(f"Detected file deletion: {deleted_file}")
                    watcher.delete_remote_file(deleted_file)
            
            file_mtimes = current_files
            
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")


def main():
    parser = argparse.ArgumentParser(description="Watch for file changes and upload to FTP server")
    parser.add_argument('--local', '-l', default='.', help='Local directory to watch (default: .)')
    parser.add_argument('--config', '-c', default=str(ROOT / '.vscode' / 'ftp-sync.json'), help='Path to ftp config JSON')
    parser.add_argument('--remote', '-r', help='Remote base path (overrides config remotePath)')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without uploading')
    parser.add_argument('--poll', action='store_true', help='Force polling mode (don\'t use watchdog)')
    args = parser.parse_args()

    try:
        # Change to project root
        os.chdir(ROOT)
        
        # Load FTPUploader class and default excludes
        FTPUploader, default_excludes = load_ftp_uploader()
        
        # Initialize uploader
        uploader = FTPUploader(Path(args.config))
        
        # Get remote base path
        remote_base = args.remote or os.environ.get('FTP_REMOTE') or uploader.config.get('remotePath', '/')
        if remote_base.startswith('./'):
            remote_base = remote_base[2:]
        remote_base = remote_base.strip('/')
        
        # Validate local directory
        local_base = Path(args.local)
        if not local_base.exists() or not local_base.is_dir():
            logger.error(f'Local directory not found: {local_base}')
            sys.exit(2)
        
        # Create file watcher
        watcher = FileWatcher(uploader, local_base, remote_base, default_excludes, args.dry_run)
        
        # Try to use watchdog first, fall back to polling
        use_watchdog = not args.poll
        
        if use_watchdog:
            try:
                run_watchdog_watcher(watcher)
            except ImportError:
                logger.info("watchdog not available, using polling mode")
                run_polling_watcher(watcher)
            except Exception as e:
                logger.warning(f"watchdog failed ({e}), falling back to polling")
                run_polling_watcher(watcher)
        else:
            run_polling_watcher(watcher)
    
    except KeyboardInterrupt:
        logger.info("File watcher stopped by user")
    except Exception as e:
        logger.error(f"File watcher failed: {e}")
        sys.exit(1)
    finally:
        # Clean up uploader connection
        try:
            if 'uploader' in locals():
                uploader.disconnect()
        except Exception:
            pass


if __name__ == '__main__':
    main()