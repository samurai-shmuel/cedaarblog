# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV SECRET_KEY Z9k65UYL0yEHCv38gk0BrB6NFjJsQZ8d

# Set work directory
WORKDIR /main_app

# Install dependencies
COPY requirements.txt /main_app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /main_app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "main_app.wsgi:application", "--bind", "0.0.0.0:8000"]
