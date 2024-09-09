# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the app
CMD ["gunicorn", "djangoProject.wsgi:application", "--bind", "0.0.0.0:8000"]
