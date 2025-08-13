#!/usr/bin/env python
"""
Database restore script for HireIQ PostgreSQL database.

This script restores PostgreSQL database backups created by db_backup.py
"""

import os
import sys
import subprocess
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

def check_backup_file(backup_file):
    """Check if backup file exists and determine its type."""
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        print(f"❌ Backup file not found: {backup_file}")
        return None
    
    # Determine backup type based on file extension
    if backup_path.suffix == '.dump':
        return 'custom'
    elif backup_path.suffix == '.sql':
        return 'plain'
    elif backup_path.is_dir():
        return 'directory'
    else:
        print(f"❌ Unknown backup file type: {backup_file}")
        return None

def drop_database_connections(db_config):
    """Drop all connections to the database before restore."""
    print("🔌 Dropping existing database connections...")
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config['password']
    
    # Connect to postgres database to run admin commands
    cmd = [
        'psql',
        '-h', db_config['host'],
        '-p', str(db_config['port']),
        '-U', db_config['user'],
        '-d', 'postgres',
        '-c', f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db_config['name']}' AND pid <> pg_backend_pid();"
    ]
    
    try:
        subprocess.run(cmd, env=env, capture_output=True, text=True, check=True)
        print("✅ Database connections dropped")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not drop all connections: {e}")

def restore_database(backup_file, backup_type=None, drop_existing=False):
    """
    Restore database from backup file.
    
    Args:
        backup_file (str): Path to backup file
        backup_type (str): Type of backup ('custom', 'plain', 'directory')
        drop_existing (bool): Whether to drop existing database first
    """
    db_config = get_db_config()
    
    if backup_type is None:
        backup_type = check_backup_file(backup_file)
        if backup_type is None:
            return False
    
    # Set environment variable for password
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config['password']
    
    # Drop existing database connections if requested
    if drop_existing:
        drop_database_connections(db_config)
    
    try:
        if backup_type == 'custom':
            # Use pg_restore for custom format
            cmd = [
                'pg_restore',
                '-h', db_config['host'],
                '-p', str(db_config['port']),
                '-U', db_config['user'],
                '-d', db_config['name'],
                '--clean',  # Clean existing objects
                '--if-exists',  # Don't error if objects don't exist
                '--no-owner',  # Skip ownership changes
                '--no-privileges',  # Skip privilege changes
                '-v',  # Verbose output
                backup_file
            ]
            
        elif backup_type == 'plain':
            # Use psql for plain SQL format
            cmd = [
                'psql',
                '-h', db_config['host'],
                '-p', str(db_config['port']),
                '-U', db_config['user'],
                '-d', db_config['name'],
                '-f', backup_file
            ]
            
        elif backup_type == 'directory':
            # Use pg_restore for directory format
            cmd = [
                'pg_restore',
                '-h', db_config['host'],
                '-p', str(db_config['port']),
                '-U', db_config['user'],
                '-d', db_config['name'],
                '--clean',
                '--if-exists',
                '--no-owner',
                '--no-privileges',
                '-v',
                backup_file
            ]
        
        print(f"🔄 Restoring {backup_type} backup: {backup_file}")
        print("This may take a few minutes...")
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database restored successfully!")
            print("\n💡 Next steps:")
            print("1. Run migrations: python manage.py migrate")
            print("2. Create superuser: python manage.py createsuperuser")
            print("3. Collect static files: python manage.py collectstatic")
            return True
        else:
            print(f"❌ Restore failed: {result.stderr}")
            if "already exists" in result.stderr:
                print("\n💡 Try using --drop-existing flag to replace existing data")
            return False
            
    except FileNotFoundError as e:
        if 'pg_restore' in str(e):
            print("❌ pg_restore not found. Please install PostgreSQL client tools.")
        elif 'psql' in str(e):
            print("❌ psql not found. Please install PostgreSQL client tools.")
        return False
    except Exception as e:
        print(f"❌ Restore failed: {str(e)}")
        return False

def list_available_backups():
    """List available backup files."""
    backup_dir = Path(__file__).parent.parent / 'backups'
    
    if not backup_dir.exists():
        print("No backup directory found.")
        return []
    
    backups = []
    for file in backup_dir.iterdir():
        if file.name.startswith('hireiq_backup_'):
            backup_type = check_backup_file(file)
            if backup_type:
                backups.append({
                    'file': str(file),
                    'name': file.name,
                    'type': backup_type,
                    'size': file.stat().st_size / 1024 / 1024 if file.is_file() else 0
                })
    
    if backups:
        print("\n📁 Available backups:")
        print("-" * 60)
        for backup in sorted(backups, key=lambda x: x['name'], reverse=True):
            size_str = f"{backup['size']:.2f} MB" if backup['size'] > 0 else "Directory"
            print(f"{backup['name']:<30} {backup['type']:<10} {size_str}")
        print("-" * 60)
    else:
        print("No backups found.")
    
    return backups

def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='HireIQ Database Restore Tool')
    parser.add_argument(
        '--file',
        required=False,
        help='Path to backup file to restore'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available backup files'
    )
    parser.add_argument(
        '--drop-existing',
        action='store_true',
        help='Drop existing database connections before restore'
    )
    parser.add_argument(
        '--type',
        choices=['custom', 'plain', 'directory'],
        help='Backup type (auto-detected if not specified)'
    )
    
    args = parser.parse_args()
    
    if args.list:
        backups = list_available_backups()
        if backups:
            print(f"\n💡 To restore a backup, use:")
            print(f"python infrastructure/scripts/db_restore.py --file backups/BACKUP_NAME")
    elif args.file:
        success = restore_database(args.file, args.type, args.drop_existing)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main() 