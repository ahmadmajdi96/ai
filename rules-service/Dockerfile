FROM python:3.11-slim
WORKDIR /app
COPY rules-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY rules-service/app.py .
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn", "app:app","--host","0.0.0.0","--port","8000"]
