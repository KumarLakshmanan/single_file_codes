#!/usr/bin/env python3
"""
ftp_upload.py

Core FTP upload functionality with support for single file and directory uploads.
Reads configuration from .vscode/ftp-sync.json and supports environment variable overrides.

Usage:
  python3 scripts/ftp_upload.py [--local LOCAL_DIR] [--config CONFIG_JSON] [--remote REMOTE_PATH] [--dry-run] [--watch]

The script will:
 - Read FTP connection settings from the config file (or environment variables)
 - Connect to the FTP server (supports FTP and FTPS based on config)
 - Create remote directories as needed recursively
 - Upload files with binary mode
 - Respect allow/ignore patterns from config
 - Log errors to `errors.txt` in repo root if anything fails
"""

import argparse
import json
import os
import ftplib
import sys
from pathlib import Path
import time
import fnmatch
from typing import List, Tuple, Dict, Optional, Union
import logging

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / '.vscode' / 'ftp-sync.json'
ERRORS_FILE = ROOT / 'errors.txt'
LOG_FILE = ROOT / 'ftp_upload.log'

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

# Default exclude patterns (relative to the local base)
DEFAULT_EXCLUDES = [
    '.git',
    '.git/**',
    '.gitignore',
    '.DS_Store',
    'node_modules',
    'node_modules/**',
    '__pycache__',
    '__pycache__/**',
    '*.pyc',
    '*.log'
]


class FTPUploader:
    """FTP Uploader class to handle all FTP operations"""
    
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or DEFAULT_CONFIG
        self.config = self._read_config()
        self.connection_info = self._get_connection_info()
        self.ftp = None
        
    def _read_config(self) -> dict:
        """Read configuration from JSON file"""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {}
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to read config {self.config_path}: {e}")
    
    def _get_connection_info(self) -> tuple:
        """Extract connection information from config and environment variables"""
        host = os.environ.get('FTP_HOST') or self.config.get('host')
        user = os.environ.get('FTP_USER') or self.config.get('username')
        passwd = os.environ.get('FTP_PASS') or self.config.get('password')
        port = int(os.environ.get('FTP_PORT') or self.config.get('port', 21))
        passive = self.config.get('passive', True)
        secure = self.config.get('secure', False)
        
        if not host or not user or not passwd:
            raise RuntimeError('Missing FTP credentials. Provide them in the config or set FTP_HOST/FTP_USER/FTP_PASS env vars.')
        
        return (host, port, user, passwd, passive, secure)
    
    def connect(self) -> ftplib.FTP:
        """Create and return FTP connection"""
        host, port, user, passwd, passive, secure = self.connection_info
        
        try:
            if secure:
                ftp = ftplib.FTP_TLS()
            else:
                ftp = ftplib.FTP()
            
            ftp.connect(host, port, timeout=30)
            ftp.login(user, passwd)
            ftp.set_pasv(passive)
            logger.info(f"Connected to FTP server: {host}:{port}")
            return ftp
        except Exception as e:
            logger.error(f"Failed to connect to FTP server: {e}")
            raise
    
    def _create_remote_directories(self, ftp: ftplib.FTP, remote_path: str) -> List[str]:
        """Create remote directories recursively, handling file conflicts"""
        deleted_conflicts = []
        
        if not remote_path or remote_path in ('/', '.'):
            return deleted_conflicts
        
        # Normalize path and split into parts
        parts = [p for p in remote_path.replace('\\', '/').split('/') if p and p not in ('.', '')]
        
        # Start from root
        ftp.cwd('/')
        
        for part in parts:
            try:
                ftp.cwd(part)
            except ftplib.error_perm:
                # Directory doesn't exist, try to create it
                try:
                    ftp.mkd(part)
                    ftp.cwd(part)
                    logger.info(f"Created remote directory: {part}")
                except ftplib.error_perm as e:
                    error_msg = str(e).lower()
                    # Check if it's a file conflict (common 550 error)
                    if '550' in error_msg or 'file exists' in error_msg or 'not a directory' in error_msg:
                        try:
                            # Remove the conflicting file
                            ftp.delete(part)
                            deleted_conflicts.append(part)
                            logger.warning(f"Deleted conflicting file to create directory: {part}")
                            
                            # Now create the directory
                            ftp.mkd(part)
                            ftp.cwd(part)
                        except Exception as del_error:
                            raise RuntimeError(f"Failed to resolve file conflict for directory '{part}': {del_error}")
                    else:
                        raise RuntimeError(f"Failed to create remote directory '{part}': {e}")
        
        return deleted_conflicts
    
    def _matches_patterns(self, path: str, patterns: List[str]) -> bool:
        """Check if path matches any of the given patterns"""
        for pattern in patterns:
            # Handle escaped dots in JSON
            try_patterns = [pattern, pattern.replace('\\.', '.')]
            for tp in try_patterns:
                if fnmatch.fnmatch(path, tp) or fnmatch.fnmatch(os.path.basename(path), tp):
                    return True
        return False
    
    def _should_upload_file(self, rel_path: str, allows: List[str], ignores: List[str]) -> bool:
        """Determine if a file should be uploaded based on allow/ignore patterns"""
        # If allow patterns exist, file must match at least one
        if allows:
            if not self._matches_patterns(rel_path, allows):
                return False
        
        # Check ignore patterns
        if self._matches_patterns(rel_path, ignores):
            return False
        
        return True
    
    def upload_file(self, local_file_path: Union[str, Path], remote_base_path: str = "", 
                   local_base_path: Union[str, Path] = None, dry_run: bool = False) -> Optional[str]:
        """
        Upload a single file to the FTP server
        
        Args:
            local_file_path: Path to the local file to upload
            remote_base_path: Base remote directory path
            local_base_path: Base local directory (to calculate relative path)
            dry_run: If True, only simulate the upload
            
        Returns:
            Error message if upload failed, None if successful
        """
        local_file_path = Path(local_file_path)
        if local_base_path:
            local_base_path = Path(local_base_path)
        else:
            local_base_path = local_file_path.parent
        
        if not local_file_path.exists() or not local_file_path.is_file():
            return f"Local file not found: {local_file_path}"
        
        try:
            # Calculate relative path
            rel_path = os.path.relpath(local_file_path, local_base_path)
            
            # Get patterns from config
            allows = self.config.get('allow', [])
            ignores = self.config.get('ignore', []) + DEFAULT_EXCLUDES
            
            # Check if file should be uploaded
            if not self._should_upload_file(rel_path, allows, ignores):
                logger.info(f"SKIP (filtered): {local_file_path}")
                return None
            
            # Calculate remote directory
            rel_dir = os.path.dirname(rel_path)
            if rel_dir and rel_dir != '.':
                remote_dir = f"{remote_base_path.strip('/')}/{rel_dir}".strip('/')
            else:
                remote_dir = remote_base_path.strip('/')
            
            if dry_run:
                logger.info(f"DRY RUN: would upload {local_file_path} -> {remote_dir}/{local_file_path.name}")
                return None
            
            # Connect if not already connected
            if not self.ftp:
                self.ftp = self.connect()
            
            # Create remote directories
            deleted_conflicts = self._create_remote_directories(self.ftp, remote_dir)
            if deleted_conflicts:
                logger.warning(f"Deleted conflicting files: {deleted_conflicts}")
            
            # Upload the file
            with open(local_file_path, 'rb') as f:
                self.ftp.storbinary(f'STOR {local_file_path.name}', f)
            
            logger.info(f"Uploaded: {local_file_path} -> {remote_dir}/{local_file_path.name}")
            return None
            
        except Exception as e:
            error_msg = f"Failed to upload {local_file_path}: {e}"
            logger.error(error_msg)
            return error_msg
    
    def upload_directory(self, local_dir_path: Union[str, Path], remote_base_path: str = "", 
                        dry_run: bool = False) -> dict:
        """
        Upload entire directory to FTP server
        
        Args:
            local_dir_path: Path to local directory to upload
            remote_base_path: Base remote directory path
            dry_run: If True, only simulate the upload
            
        Returns:
            Dictionary with upload statistics and any errors
        """
        local_dir_path = Path(local_dir_path)
        
        if not local_dir_path.exists() or not local_dir_path.is_dir():
            raise RuntimeError(f"Local directory not found: {local_dir_path}")
        
        stats = {
            'uploaded_count': 0,
            'skipped_count': 0,
            'error_count': 0,
            'errors': [],
            'deleted_conflicts': []
        }
        
        # Get patterns from config
        allows = self.config.get('allow', [])
        ignores = self.config.get('ignore', []) + DEFAULT_EXCLUDES
        
        try:
            # Connect if not already connected
            if not self.ftp:
                self.ftp = self.connect()
            
            # Walk through all files in directory
            for root, dirs, files in os.walk(local_dir_path):
                for filename in files:
                    local_file_path = Path(root) / filename
                    
                    # Calculate relative path
                    rel_path = os.path.relpath(local_file_path, local_dir_path)
                    
                    # Check if file should be uploaded
                    if not self._should_upload_file(rel_path, allows, ignores):
                        stats['skipped_count'] += 1
                        logger.debug(f"SKIP (filtered): {rel_path}")
                        continue
                    
                    # Upload the file
                    error = self.upload_file(local_file_path, remote_base_path, local_dir_path, dry_run)
                    
                    if error:
                        stats['error_count'] += 1
                        stats['errors'].append(error)
                    else:
                        stats['uploaded_count'] += 1
            
            logger.info(f"Directory upload complete. Uploaded: {stats['uploaded_count']}, "
                       f"Skipped: {stats['skipped_count']}, Errors: {stats['error_count']}")
            
        except Exception as e:
            error_msg = f"Directory upload failed: {e}"
            stats['errors'].append(error_msg)
            logger.error(error_msg)
        
        return stats
    
    def disconnect(self):
        """Close FTP connection"""
        if self.ftp:
            try:
                self.ftp.quit()
                logger.info("Disconnected from FTP server")
            except Exception:
                try:
                    self.ftp.close()
                except Exception:
                    pass
            finally:
                self.ftp = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


def main():
    parser = argparse.ArgumentParser(description="Upload files to FTP server")
    parser.add_argument('--local', '-l', default='.', help='Local directory to upload (default: .)')
    parser.add_argument('--config', '-c', default=str(DEFAULT_CONFIG), help='Path to ftp config JSON')
    parser.add_argument('--remote', '-r', help='Remote base path (overrides config remotePath)')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without uploading')
    parser.add_argument('--watch', '-w', action='store_true', help='Watch local dir and upload changed files (deprecated - use onsave_sync.py)')
    args = parser.parse_args()

    try:
        # Initialize uploader
        uploader = FTPUploader(Path(args.config))
        
        # Get remote base path
        remote_base = args.remote or os.environ.get('FTP_REMOTE') or uploader.config.get('remotePath', '/')
        if remote_base.startswith('./'):
            remote_base = remote_base[2:]
        remote_base = remote_base.strip('/')
        
        local_path = Path(args.local)
        
        if args.watch:
            logger.warning("--watch flag is deprecated. Use onsave_sync.py for file watching functionality.")
            return
        
        with uploader:
            if local_path.is_file():
                # Upload single file
                error = uploader.upload_file(local_path, remote_base, dry_run=args.dry_run)
                if error:
                    logger.error(error)
                    sys.exit(1)
            else:
                # Upload directory
                stats = uploader.upload_directory(local_path, remote_base, dry_run=args.dry_run)
                
                if stats['errors']:
                    # Write errors to file
                    with open(ERRORS_FILE, 'a', encoding='utf-8') as ef:
                        for error in stats['errors']:
                            ef.write(f"{error}\n")
                    
                    logger.error(f"Upload completed with {stats['error_count']} errors. See {ERRORS_FILE}")
                    sys.exit(1)
        
        logger.info("Upload completed successfully")
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()