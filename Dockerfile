# Use a slim Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code from src/ to /app/src/
COPY src/ ./src/

# Expose port 5000 for the Flask server
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=src/load_balancer.py

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
