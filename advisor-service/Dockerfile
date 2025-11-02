FROM python:3.11-slim
WORKDIR /app
COPY advisor-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY advisor-service/app.py advisor-service/prompt_builder.py advisor-service/merge_context.py ./
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
