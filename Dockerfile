# Use an official Python image with build tools
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libssl-dev \
    libffi-dev \
    cargo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your project
COPY . .

# Expose the port your app runs on (adjust if needed)
EXPOSE 8000

# CMD can be changed based on your framework (e.g., Django, Flask, FastAPI)
# Example for Django
CMD ["gunicorn", "projectname.wsgi:application", "--bind", "0.0.0.0:8000"]
