# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./server/requirements.txt /app/requirements.txt

# Install Flask and OpenAI libraries from the requirements file
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the Flask application code into the container
COPY ./server/FlaskServer.py /app/app.py

# Create the correct directory structure for your db handler
COPY ./db /app/services/db

# Copy the test file into the container
COPY ./test_db.py /app/services/test_db.py

# Expose port 5000 for the Flask application
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]
