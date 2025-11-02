FROM python:3.11-slim
WORKDIR /app
COPY decision-orchestrator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY decision-orchestrator/app.py decision-orchestrator/aggregator.py ./
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
