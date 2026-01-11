import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Create default superuser and staff user'

    def handle(self, *args, **options):
        # Superuser details from env or defaults
        su_username = os.getenv('SUPERUSER_NAME', 'asher_wele')
        su_email = os.getenv('SUPERUSER_EMAIL', 'asher@gmail.com')
        su_password = os.getenv('SUPERUSER_PASSWORD', '1234')

        # Staff user details
        staff_username = os.getenv('STAFF_NAME', 'Ogan')
        staff_password = os.getenv('STAFF_PASSWORD', '4321')

        # Create Superuser
        if not User.objects.filter(username=su_username).exists():
            try:
                User.objects.create_superuser(
                    username=su_username,
                    email=su_email,
                    password=su_password
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {su_username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))
        else:
            # Update password if exists (to ensure the user can log in with provided credentials)
            u = User.objects.get(username=su_username)
            u.set_password(su_password)
            u.save()
            self.stdout.write(self.style.WARNING(f'Superuser {su_username} already exists. Password updated.'))

        # Create Staff User
        if not User.objects.filter(username=staff_username).exists():
            try:
                User.objects.create_user(
                    username=staff_username,
                    password=staff_password,
                    is_staff=True
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created staff user: {staff_username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating staff user: {e}'))
        else:
            u = User.objects.get(username=staff_username)
            u.set_password(staff_password)
            u.save()
            self.stdout.write(self.style.WARNING(f'Staff user {staff_username} already exists. Password updated.'))
