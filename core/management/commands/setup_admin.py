from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

class Command(BaseCommand):
    help = 'Create or update superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'admin_piyapat'
        email = 'donutpiyapat@gmail.com'
        password = 'Admin04072026'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created new superuser: {username}'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated password for existing superuser: {username}'))

    help = 'Enable pg_trgm extension in PostgreSQL'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        self.stdout.write(self.style.SUCCESS('Successfully enabled pg_trgm extension'))