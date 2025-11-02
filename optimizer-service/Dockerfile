FROM python:3.11-slim
WORKDIR /app
COPY optimizer-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY optimizer-service/app.py optimizer-service/cost_optimizer.py optimizer-service/workflow_optimizer.py optimizer-service/bottleneck_optimizer.py optimizer-service/risk_model.py ./
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
