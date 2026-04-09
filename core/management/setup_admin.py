from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create or update superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = 'admin'
        email = 'admin@gmail.com'
        password = 'Admin123456'  # 🔥 เปลี่ยนทีหลังได้

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Password updated'))