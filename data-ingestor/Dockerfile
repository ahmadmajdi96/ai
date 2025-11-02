FROM python:3.11-slim
WORKDIR /app
COPY data-ingestor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY data-ingestor/app.py data-ingestor/normalizer.py data-ingestor/storage.py ./
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
