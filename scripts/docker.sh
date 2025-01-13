#!/bin/sh

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Apply database migrations
python manage.py migrate

# Check if superuser already exists
EXISTING_USER=$(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(email='$SUPERUSER_EMAIL').exists())")

if [ "$EXISTING_USER" != "True" ]; then
    # Create a superuser using environment variables
    echo "from django.contrib.auth.models import User; \
    User.objects.create_superuser('$SUPERUSER_EMAIL', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell
else
    echo "Superuser already exists, skipping creation."
fi

# Start the Django server
exec python manage.py runserver 0.0.0.0:8000
