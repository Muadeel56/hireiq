#!/usr/bin/env python
"""
Database backup script for HireIQ PostgreSQL database.

This script creates backups of the PostgreSQL database with timestamps
and provides options for different backup formats.
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from decouple import config

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hireiq_backend.settings')
import django
django.setup()

def get_db_config():
    """Get database configuration from Django settings."""
    from django.conf import settings
    db_config = settings.DATABASES['default']
    return {
        'host': db_config.get('HOST', 'localhost'),
        'port': db_config.get('PORT', '5432'),
        'name': db_config['NAME'],
        'user': db_config['USER'],
        'password': db_config['PASSWORD'],
    }

def create_backup_directory():
    """Create backup directory if it doesn't exist."""
    backup_dir = Path(__file__).parent.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    return backup_dir

def backup_database(format_type='custom'):
    """
    Create a database backup.
    
    Args:
        format_type (str): Backup format ('custom', 'plain', 'directory')
    """
    db_config = get_db_config()
    backup_dir = create_backup_directory()
    
    # Generate timestamp for backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Set backup filename based on format
    if format_type == 'custom':
        backup_file = backup_dir / f"hireiq_backup_{timestamp}.dump"
        format_flag = '-Fc'
    elif format_type == 'plain':
        backup_file = backup_dir / f"hireiq_backup_{timestamp}.sql"
        format_flag = '-Fp'
    elif format_type == 'directory':
        backup_file = backup_dir / f"hireiq_backup_{timestamp}"
        format_flag = '-Fd'
    else:
        raise ValueError("Invalid format type. Use 'custom', 'plain', or 'directory'")
    
    # Set environment variable for password
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config['password']
    
    # Build pg_dump command
    cmd = [
        'pg_dump',
        format_flag,
        '-h', db_config['host'],
        '-p', str(db_config['port']),
        '-U', db_config['user'],
        '-d', db_config['name'],
        '-f', str(backup_file)
    ]
    
    try:
        print(f"Creating {format_type} backup...")
        print(f"Backup file: {backup_file}")
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Backup created successfully: {backup_file}")
            print(f"Backup size: {backup_file.stat().st_size / 1024 / 1024:.2f} MB")
            return str(backup_file)
        else:
            print(f"❌ Backup failed: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ pg_dump not found. Please install PostgreSQL client tools.")
        return None
    except Exception as e:
        print(f"❌ Backup failed: {str(e)}")
        return None

def list_backups():
    """List all available backups."""
    backup_dir = create_backup_directory()
    backups = []
    
    for file in backup_dir.iterdir():
        if file.name.startswith('hireiq_backup_'):
            backups.append({
                'file': file,
                'name': file.name,
                'size': file.stat().st_size / 1024 / 1024,  # Size in MB
                'created': datetime.fromtimestamp(file.stat().st_mtime)
            })
    
    # Sort by creation time (newest first)
    backups.sort(key=lambda x: x['created'], reverse=True)
    
    if backups:
        print("\n📁 Available backups:")
        print("-" * 80)
        for backup in backups:
            print(f"{backup['name']:<30} {backup['size']:>8.2f} MB {backup['created']}")
    else:
        print("No backups found.")
    
    return backups

def cleanup_old_backups(keep_count=10):
    """Remove old backups, keeping only the specified number."""
    backups = list_backups()
    
    if len(backups) > keep_count:
        to_remove = backups[keep_count:]
        print(f"\n🧹 Cleaning up old backups (keeping {keep_count} most recent)...")
        
        for backup in to_remove:
            try:
                if backup['file'].is_file():
                    backup['file'].unlink()
                elif backup['file'].is_dir():
                    import shutil
                    shutil.rmtree(backup['file'])
                print(f"Removed: {backup['name']}")
            except Exception as e:
                print(f"Failed to remove {backup['name']}: {str(e)}")

def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='HireIQ Database Backup Tool')
    parser.add_argument(
        '--format', 
        choices=['custom', 'plain', 'directory'],
        default='custom',
        help='Backup format (default: custom)'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available backups'
    )
    parser.add_argument(
        '--cleanup',
        type=int,
        metavar='N',
        help='Keep only N most recent backups'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_backups()
    elif args.cleanup is not None:
        cleanup_old_backups(args.cleanup)
    else:
        backup_file = backup_database(args.format)
        if backup_file:
            print(f"\n💡 To restore this backup, use:")
            if args.format == 'custom':
                print(f"python scripts/db_restore.py --file {backup_file}")
            elif args.format == 'plain':
                print(f"psql -h localhost -U hireiq_user -d hireiq_db < {backup_file}")

if __name__ == '__main__':
    main() 