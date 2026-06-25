# Use a slim Python image to keep the size down
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (needed for some vector DB / ML libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Create the directory for the persistent vector DB
RUN mkdir -p /app/my_vector_db

# Define a specific path for the cache
ENV HF_HOME=/app/hf_cache
RUN mkdir -p /app/hf_cache

# Expose the port Gradio runs on
EXPOSE 7860

# Set environment variable to ensure Gradio listens on all interfaces
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Create a non-root user
RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /app
# Run container as non-root user
USER appuser

# Command to run your app
CMD ["python", "app.py"]