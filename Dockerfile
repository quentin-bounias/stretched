# Base Python image
FROM python:3.11-slim

# Install dependencies
RUN pip install fastapi uvicorn python-multipart pillow

# Set working directory
WORKDIR /app

# Copy backend (to be added soon)
COPY backend /app/backend

# Copy frontend files
COPY frontend /app/frontend

# Expose port for backend
EXPOSE 8000

# Command to run FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
