FROM python:3.11-slim
WORKDIR /app
COPY rag-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY rag-service/app.py rag-service/embedder.py rag-service/retriever.py ./
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
