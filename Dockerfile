# Use a slim version of the Python image for a smaller footprint
FROM python:3.9-slim

# Set environment variables to avoid Python writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set a working directory
WORKDIR /app

# Install system dependencies required for libraries like Pillow and pytesseract
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt first to install dependencies
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application using FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
