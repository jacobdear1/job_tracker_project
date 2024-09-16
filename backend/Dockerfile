# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /backend

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to /app in the container
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Define environment variable
ENV UVICORN_CMD="uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Run the application
CMD ["sh", "-c", "$UVICORN_CMD"]
