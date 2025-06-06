# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies (Installs libpq-dev for PostgreSQL; psycopg2 requires it)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY ./app ./app

# Expose the API port
EXPOSE 8000

# Command to run the app
# Includes --reload for hot-reloading during development (can remove for production).
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

