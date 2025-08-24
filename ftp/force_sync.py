#!/usr/bin/env python3
"""
force_sync.py

Force synchronization script that uploads all files from the local directory
to the remote FTP server using the FTPUploader class from ftp_upload.py.

This script provides a convenient way to perform a complete upload of all files
in the project, respecting the allow/ignore patterns from ftp-sync.json.

Usage:
  python3 scripts/force_sync.py [--local LOCAL_DIR] [--config CONFIG_JSON] [--remote REMOTE_PATH] [--dry-run]

This script validates FTP credentials and performs a one-shot complete upload.
"""

import sys
import os
import argparse
from pathlib import Path
import logging

ROOT = Path(__file__).resolve().parents[1]
FTP_UPLOAD_PATH = ROOT / 'scripts' / 'ftp_upload.py'
LOG_FILE = ROOT / 'force_sync.log'

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
    return module.FTPUploader


def validate_credentials(config_path: Path):
    """Validate that FTP credentials are available"""
    config_exists = config_path.exists()
    host = os.environ.get('FTP_HOST')
    user = os.environ.get('FTP_USER')
    passwd = os.environ.get('FTP_PASS')
    
    has_env_credentials = bool(host and user and passwd)
    
    if not has_env_credentials and not config_exists:
        logger.error('Missing FTP credentials. Provide them in the config file or set FTP_HOST/FTP_USER/FTP_PASS environment variables.')
        return False
    
    if config_exists:
        try:
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            config_host = config.get('host')
            config_user = config.get('username')  
            config_pass = config.get('password')
            
            if not has_env_credentials and not (config_host and config_user and config_pass):
                logger.error('Incomplete FTP credentials in config file.')
                return False
                
        except Exception as e:
            logger.error(f'Error reading config file: {e}')
            return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Force upload all files to FTP server")
    parser.add_argument('--local', '-l', default='.', help='Local directory to upload (default: . - project root)')
    parser.add_argument('--config', '-c', default=str(ROOT / '.vscode' / 'ftp-sync.json'), help='Path to ftp config JSON')
    parser.add_argument('--remote', '-r', help='Remote base path (overrides config remotePath)')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without uploading')
    args = parser.parse_args()

    try:
        # Change to project root
        os.chdir(ROOT)
        
        # Validate credentials before attempting upload
        config_path = Path(args.config)
        if not validate_credentials(config_path):
            sys.exit(2)
        
        # Load FTPUploader class
        FTPUploader = load_ftp_uploader()
        
        # Initialize uploader
        uploader = FTPUploader(config_path)
        
        # Get remote base path
        remote_base = args.remote or os.environ.get('FTP_REMOTE') or uploader.config.get('remotePath', '/')
        if remote_base.startswith('./'):
            remote_base = remote_base[2:]
        remote_base = remote_base.strip('/')
        
        # Validate local directory
        local_path = Path(args.local)
        if not local_path.exists():
            logger.error(f'Local directory not found: {local_path}')
            sys.exit(2)
        
        logger.info(f"Starting force sync: {local_path} -> {remote_base}")
        logger.info(f"Dry run: {args.dry_run}")
        
        # Perform the upload
        with uploader:
            if local_path.is_file():
                # Upload single file
                logger.info("Uploading single file...")
                error = uploader.upload_file(local_path, remote_base, dry_run=args.dry_run)
                if error:
                    logger.error(f"Upload failed: {error}")
                    sys.exit(1)
                else:
                    logger.info("Single file upload completed successfully")
            else:
                # Upload entire directory
                logger.info("Uploading directory...")
                stats = uploader.upload_directory(local_path, remote_base, dry_run=args.dry_run)
                
                # Log summary
                logger.info(f"Upload summary:")
                logger.info(f"  - Files uploaded: {stats['uploaded_count']}")
                logger.info(f"  - Files skipped: {stats['skipped_count']}")
                logger.info(f"  - Errors: {stats['error_count']}")
                
                if stats['deleted_conflicts']:
                    logger.warning(f"  - Deleted conflicting files: {stats['deleted_conflicts']}")
                
                if stats['errors']:
                    logger.error("Errors occurred during upload:")
                    for error in stats['errors']:
                        logger.error(f"  - {error}")
                    
                    # Write errors to file
                    error_file = ROOT / 'force_sync_errors.txt'
                    with open(error_file, 'w', encoding='utf-8') as ef:
                        for error in stats['errors']:
                            ef.write(f"{error}\n")
                    
                    logger.error(f"Detailed errors written to: {error_file}")
                    sys.exit(1)
                else:
                    logger.info("Directory upload completed successfully")
    
    except KeyboardInterrupt:
        logger.info("Force sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Force sync failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()