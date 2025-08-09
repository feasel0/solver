FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends     libnss3 libatk-bridge2.0-0 libxkbcommon0 libxcomposite1     libxdamage1 libxfixes3 libgbm1 libasound2 libxrandr2 libatk1.0-0     libgtk-3-0 libxshmfence1 fonts-liberation xdg-utils wget     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
