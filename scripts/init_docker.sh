#!/bin/sh

# Apply database migrations
python manage.py migrate

# Create a superuser (you can add checks to prevent duplicate creation)
echo "from django.contrib.auth.models import User; \
User.objects.create_superuser('prop', 'prop@gmail.com', 'prop')" | python manage.py shell

# Start the Django server
exec python manage.py runserver 0.0.0.0:8000