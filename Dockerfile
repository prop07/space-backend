# Use an official Python base image
FROM python:3.11-slim


# Set the working directory in the container
WORKDIR /app

# Copy requirements directly into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Apply database migrations
RUN python manage.py migrate

# Expose port 8000 to allow access from outside the container
EXPOSE 8000

# Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
