FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir mitmproxy

COPY cache-proxy.py .

EXPOSE 3000

CMD ["python3", "cache-proxy.py"]
