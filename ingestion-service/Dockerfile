FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# requirements.txt from main -> check if local should be used instead
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Python-Code from ingestion-service/src/ copied to /app/src/ in the container
COPY ingestion-service/src/ ./src/

# Command to run the main.py script in the container
CMD ["python", "src/main.py"]