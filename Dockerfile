# Cloud Cost Optimization Dashboard
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY data.py .
COPY layout.py .
COPY assets/ ./assets/

# Expose port
EXPOSE 8050

# Run the application
CMD ["python", "app.py"]
