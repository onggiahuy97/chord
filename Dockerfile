FROM python:3.12

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY main.py .

# Create non-root user
RUN useradd -m app
USER app

# Expose new port
EXPOSE 5001

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=5001

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
