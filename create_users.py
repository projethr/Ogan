import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ogan_project.settings')
django.setup()

from django.contrib.auth.models import User

# Create Superuser asher
if not User.objects.filter(username='asher').exists():
    User.objects.create_superuser('asher', 'weleasher@gmail.com', '1234')
    print("Superuser 'asher' created.")
else:
    print("Superuser 'asher' already exists.")

# Create Staff OGAN
if not User.objects.filter(username='OGAN').exists():
    user = User.objects.create_user('OGAN', '', '4321')
    user.is_staff = True
    user.save()
    print("Staff user 'OGAN' created.")
else:
    print("Staff user 'OGAN' already exists.")
