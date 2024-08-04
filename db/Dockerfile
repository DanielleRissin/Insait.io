# Use the latest official PostgreSQL image from the Docker Hub
FROM postgres:latest


ENV PYTHONUNBUFFERED=1

# Expose the default PostgreSQL port
EXPOSE 5432

# Set the working directory
WORKDIR /app

# Install Python and dependencies, including the virtual environment package
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create and activate a virtual environment
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements file and install Python packages within the virtual environment
COPY ./db/requirements.txt /app/service-requirements.txt
RUN pip install --no-cache-dir -r /app/service-requirements.txt

# Copy Python script to the working directory
COPY ./db/db_handler.py /app/main.py

# Default command to run PostgreSQL
CMD ["postgres"]
