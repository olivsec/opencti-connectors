FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libmagic1 netcat-openbsd \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY main.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

RUN useradd -m appuser
USER appuser

ENTRYPOINT ["./entrypoint.sh"]
