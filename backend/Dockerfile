FROM python:3.10-slim

WORKDIR /app

# System deps for OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Model will be mounted via docker-compose volume
# but also support a local copy
COPY modelo_efficientnet_final.keras ./modelo_efficientnet_final.keras

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
