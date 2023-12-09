# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app/
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Celery to run in production
ENV DJANGO_SETTINGS_MODULE=jyn_pathshala.settings
# ENV DJANGO_SETTINGS_MODULE=jyn_pathshala.settings.production

# Collect static files
# RUN python manage.py collectstatic --noinput

# Run Django migrations
RUN python manage.py migrate

# Start Django development server
# CMD ["gunicorn", "jyn_pathshala.wsgi:application", "--bind", "0.0.0.0:8000"]
