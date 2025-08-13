from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import connection


class Command(BaseCommand):
    help = 'Set up the development environment'

    def handle(self, *args, **options):
        self.stdout.write('Setting up development environment...')
        
        # Create necessary directories
        import os
        from pathlib import Path
        
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        logs_dir = base_dir / 'logs'
        media_dir = base_dir / 'media'
        static_dir = base_dir / 'staticfiles'
        
        for directory in [logs_dir, media_dir, static_dir]:
            directory.mkdir(exist_ok=True)
            self.stdout.write(f'Created directory: {directory}')
        
        # Run migrations
        self.stdout.write('Running migrations...')
        call_command('migrate')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser(
                username='admin',
                email='admin@hireiq.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created: admin/admin123')
            )
        else:
            self.stdout.write('Superuser already exists')
        
        # Collect static files
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput')
        
        self.stdout.write(
            self.style.SUCCESS('Development environment setup complete!')
        ) 