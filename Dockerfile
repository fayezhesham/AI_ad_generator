# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the ports used by FastAPI and Streamlit
EXPOSE 8000 8501

# Copy the supervisord configuration file to the correct location
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf



# Start Supervisor, which in turn will launch FastAPI and Streamlit
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
