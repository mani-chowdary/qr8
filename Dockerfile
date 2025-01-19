# Use an official Python runtime as the base image
FROM python:3.11-slim

# Install system dependencies (including zbar)
RUN apt-get update && apt-get install -y libzbar0

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the Python dependencies (make sure you have a requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for Flask (or whichever port your app runs on)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]


