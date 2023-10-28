
import os

from django.core.management.base import BaseCommand

from config import settings
from team_production_system.models import CustomUser


# To run this management command:
# python manage.py add_superuser
class Command(BaseCommand):
    help = "Create a superuser on Render"

    def handle(self, *args, **options):
        if os.environ.get('RENDER'):
          user, created = CustomUser.objects.get_or_create(
                username=settings.DJANGO_SUPERUSER_USERNAME
            )
          if created:
            user.email = settings.DJANGO_SUPERUSER_EMAIL
            user.set_password(settings.DJANGO_SUPERUSER_PASSWORD)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            msg = self.style.SUCCESS(f"Superuser {settings.DJANGO_SUPERUSER_USERNAME} added to database.")
          else:
            msg = self.style.WARNING(f"Superuser {settings.DJANGO_SUPERUSER_USERNAME} already exists.")
          self.stdout.write(msg)