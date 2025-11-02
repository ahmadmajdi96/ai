FROM python:3.11-slim
WORKDIR /app
COPY analytics-engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY common_lib ./common_lib
COPY analytics-engine/app.py analytics-engine/kpi_calculations.py analytics-engine/bottleneck.py ./
ENV PYTHONPATH=/app:/app/common_lib
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
