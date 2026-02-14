# Stratus — Self-Service Streaming Data Platform

A modular, cloud-native streaming platform enabling teams to onboard real-time data pipelines with built-in governance, observability, and lakehouse integration.

---

## 🏗 Architecture Overview

Stratus follows an event-driven architecture:

- Kafka for distributed event ingestion
- Python producers & consumers
- Dockerized services
- Structured streaming processing layer
- Designed for integration with lakehouse systems (Delta/Iceberg/Snowflake)

---

## 📦 Project Structure

```
consumer/
docker/
processor/
producer/
streaming_jobs/
```

---

## ⚙️ Core Capabilities

- Replay-safe streaming pipelines
- Decoupled producer-consumer model
- Containerized microservices
- Config-driven Kafka topic management
- Extensible processing layer
- Designed for observability integration

---

## 🚀 Getting Started

### 1️⃣ Start Infrastructure

```bash
docker-compose up -d
```

### 2️⃣ Run Producer

```bash
python producer/producer.py
```

### 3️⃣ Run Consumer / Processor

```bash
python consumer/consumer.py
```

---

## 📊 Observability Roadmap

Planned enhancements:

- Structured logging
- Prometheus metrics export
- Health endpoints
- Lag monitoring
- Centralized log aggregation

---

## 🧠 Engineering Principles

- Event-driven architecture
- Idempotent processing
- Container-first design
- Separation of concerns
- Platform extensibility

---

## 🛠 Tech Stack

- Python
- Apache Kafka
- Docker
- Structured Streaming
- Lakehouse-ready design

---

## 👨‍💻 Author

Srikar Reddy Maddi  
Senior Data Engineer | Streaming Systems | Lakehouse Architectures
