FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY server.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "server.py"]
