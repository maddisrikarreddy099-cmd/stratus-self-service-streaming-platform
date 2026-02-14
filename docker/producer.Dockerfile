FROM python:3.11-slim

WORKDIR /app

COPY streaming_jobs/ ./streaming_jobs

RUN pip install -r streaming_jobs/kafka_python_demo/requirements.txt

CMD ["python", "-m", "streaming_jobs.kafka_python_demo.producers.producer"]
