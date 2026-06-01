# Use official Python slim image for smaller footprint
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (cached layer if requirements unchanged)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Create non-root user for security best practice
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Expose port
EXPOSE 5000

# Run with gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
