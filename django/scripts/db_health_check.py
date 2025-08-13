#!/usr/bin/env python
"""
Database health check script for HireIQ PostgreSQL database.

This script checks database connectivity, performance metrics, and provides
health status information for monitoring purposes.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hireiq_backend.settings')
import django
django.setup()

from django.db import connection, connections
from django.core.management.color import make_style
from django.conf import settings

style = make_style()

def check_database_connection():
    """Check if database connection is working."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                return True, "Database connection successful"
            else:
                return False, "Database connection failed - unexpected result"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

def get_database_info():
    """Get basic database information."""
    try:
        with connection.cursor() as cursor:
            # Get PostgreSQL version
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            
            # Get database size
            cursor.execute("""
                SELECT pg_size_pretty(pg_database_size(%s))
            """, [settings.DATABASES['default']['NAME']])
            db_size = cursor.fetchone()[0]
            
            # Get connection count
            cursor.execute("""
                SELECT count(*) FROM pg_stat_activity 
                WHERE datname = %s
            """, [settings.DATABASES['default']['NAME']])
            connection_count = cursor.fetchone()[0]
            
            return {
                'version': version.split(',')[0],  # Get just the version part
                'size': db_size,
                'connections': connection_count
            }
    except Exception as e:
        return {'error': str(e)}

def check_database_performance():
    """Check database performance metrics."""
    try:
        with connection.cursor() as cursor:
            # Check connection latency
            start_time = time.time()
            cursor.execute("SELECT NOW()")
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Check for long running queries
            cursor.execute("""
                SELECT count(*) FROM pg_stat_activity 
                WHERE state = 'active' 
                AND query_start < NOW() - INTERVAL '1 minute'
                AND datname = %s
            """, [settings.DATABASES['default']['NAME']])
            long_queries = cursor.fetchone()[0]
            
            # Check for locks
            cursor.execute("""
                SELECT count(*) FROM pg_locks 
                WHERE NOT granted
            """)
            blocked_queries = cursor.fetchone()[0]
            
            return {
                'latency_ms': round(latency, 2),
                'long_running_queries': long_queries,
                'blocked_queries': blocked_queries
            }
    except Exception as e:
        return {'error': str(e)}

def check_migrations_status():
    """Check if there are unapplied migrations."""
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.showmigrations import Command
        from io import StringIO
        import sys
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Run showmigrations command
            cmd = Command()
            cmd.handle(verbosity=0)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout
        
        # Check if there are any unapplied migrations
        unapplied = []
        for line in output.split('\n'):
            if '[ ]' in line:  # Unapplied migration
                unapplied.append(line.strip())
        
        return {
            'unapplied_count': len(unapplied),
            'unapplied_migrations': unapplied[:5]  # Show first 5
        }
    except Exception as e:
        return {'error': str(e)}

def run_health_check(verbose=False):
    """Run comprehensive health check."""
    print("🏥 HireIQ Database Health Check")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check database connection
    print("🔌 Database Connection:")
    conn_status, conn_message = check_database_connection()
    if conn_status:
        print(style.SUCCESS(f"  ✅ {conn_message}"))
    else:
        print(style.ERROR(f"  ❌ {conn_message}"))
        return False
    
    # Get database info
    print("\n📊 Database Information:")
    db_info = get_database_info()
    if 'error' not in db_info:
        print(f"  Version: {db_info['version']}")
        print(f"  Size: {db_info['size']}")
        print(f"  Active Connections: {db_info['connections']}")
    else:
        print(style.ERROR(f"  ❌ Error getting database info: {db_info['error']}"))
    
    # Check performance
    print("\n⚡ Performance Metrics:")
    perf_info = check_database_performance()
    if 'error' not in perf_info:
        latency = perf_info['latency_ms']
        if latency < 10:
            latency_status = style.SUCCESS(f"✅ {latency}ms (Excellent)")
        elif latency < 50:
            latency_status = style.WARNING(f"⚠️  {latency}ms (Good)")
        else:
            latency_status = style.ERROR(f"❌ {latency}ms (Slow)")
        
        print(f"  Query Latency: {latency_status}")
        print(f"  Long Running Queries: {perf_info['long_running_queries']}")
        print(f"  Blocked Queries: {perf_info['blocked_queries']}")
        
        if perf_info['long_running_queries'] > 0:
            print(style.WARNING("  ⚠️  Warning: Long running queries detected"))
        if perf_info['blocked_queries'] > 0:
            print(style.ERROR("  ❌ Warning: Blocked queries detected"))
    else:
        print(style.ERROR(f"  ❌ Error getting performance metrics: {perf_info['error']}"))
    
    # Check migrations
    print("\n🔄 Migration Status:")
    migration_info = check_migrations_status()
    if 'error' not in migration_info:
        if migration_info['unapplied_count'] == 0:
            print(style.SUCCESS("  ✅ All migrations applied"))
        else:
            print(style.WARNING(f"  ⚠️  {migration_info['unapplied_count']} unapplied migrations"))
            if verbose and migration_info['unapplied_migrations']:
                print("  Unapplied migrations:")
                for migration in migration_info['unapplied_migrations']:
                    print(f"    {migration}")
    else:
        print(style.ERROR(f"  ❌ Error checking migrations: {migration_info['error']}"))
    
    print("\n" + "=" * 50)
    
    # Overall health status
    overall_healthy = (
        conn_status and 
        'error' not in db_info and 
        'error' not in perf_info and
        perf_info.get('latency_ms', 0) < 100 and
        perf_info.get('blocked_queries', 0) == 0
    )
    
    if overall_healthy:
        print(style.SUCCESS("🎉 Overall Status: HEALTHY"))
    else:
        print(style.ERROR("⚠️  Overall Status: NEEDS ATTENTION"))
    
    return overall_healthy

def main():
    """Main function to handle command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='HireIQ Database Health Check')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    parser.add_argument(
        '--exit-code',
        action='store_true',
        help='Exit with non-zero code if unhealthy'
    )
    
    args = parser.parse_args()
    
    if args.json:
        import json
        
        # Collect all health data
        conn_status, conn_message = check_database_connection()
        db_info = get_database_info()
        perf_info = check_database_performance()
        migration_info = check_migrations_status()
        
        health_data = {
            'timestamp': datetime.now().isoformat(),
            'connection': {
                'status': conn_status,
                'message': conn_message
            },
            'database_info': db_info,
            'performance': perf_info,
            'migrations': migration_info,
            'healthy': conn_status and 'error' not in db_info and 'error' not in perf_info
        }
        
        print(json.dumps(health_data, indent=2))
        
        if args.exit_code and not health_data['healthy']:
            sys.exit(1)
    else:
        healthy = run_health_check(args.verbose)
        
        if args.exit_code and not healthy:
            sys.exit(1)

if __name__ == '__main__':
    main() 