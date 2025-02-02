# Use Python base image
FROM python:3.9

# Install system dependencies (Nginx)
RUN apt-get update && apt-get install -y nginx gunicorn && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application files into the container
ADD /app /app

# Install dependencies in a virtual environment
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt


COPY nginx.conf /etc/nginx/sites-available/default
EXPOSE 80
CMD ["/bin/sh", "-c", "service nginx restart && . venv/bin/activate && gunicorn --chdir /app app:app -b 0.0.0.0:5000"]

