import random
from django.core.management.base import BaseCommand

# Change this to reflect your app's name and name of your custom User model
from team_production_system.models import User
from config import settings  # Change this to reflect your app's name


# To run this management command:
# python manage.py add_superuser
class Command(BaseCommand):
    help = "Create a superuser in production"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            user, created = User.objects.get_or_create(
                username=settings.DJANGO_SUPERUSER_USERNAME
            )
            if created:
                user.email = settings.DJANGO_SUPERUSER_EMAIL
                user.set_password(settings.DJANGO_SUPERUSER_PASSWORD)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                msg = self.style.SUCCESS(
                    f"Superuser {settings.DJANGO_SUPERUSER_USERNAME} added to database.")
            else:
                msg = self.style.WARNING(
                    f"Superuser {settings.DJANGO_SUPERUSER_USERNAME} already exists.")
            self.stdout.write(msg)
