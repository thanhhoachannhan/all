
import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Migrate database, create superuser, and then run server'

    def handle(self, *args, **options):
        self.stdout.write('Running makemigrations...')
        call_command('makemigrations', 'core')

        self.stdout.write('Running migrations...')
        call_command('migrate')

        # self.stdout.write('Dump data...')
        # os.system('python manage.py loaddata data.json')

        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

        self.stdout.write('Starting server...')
        os.system('python manage.py runserver 0:2000')
