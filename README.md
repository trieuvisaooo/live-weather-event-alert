# 🌩️ Live Weather Event Alert System

A real-time system that ingests weather data from the OpenWeatherMap API, detects extreme weather events using Spark Structured Streaming, pushes notifications via email, and visualizes alerts in a live Streamlit dashboard.

---

## 🚀 Features

- 🔄 Real-time ingestion of weather data from multiple cities
- 🧠 Stream processing and event detection with Apache Spark
- 🔔 Email notifications for extreme weather (e.g., heatwave, storm)
- 📊 Interactive dashboard built with Streamlit
- 🐳 Fully containerized with Docker and docker-compose

---

## 📦 Tech Stack

| Layer         | Tools                               |
|---------------|-------------------------------------|
| Ingestion     | Python + OpenWeatherMap API         |
| Messaging     | Apache Kafka                        |
| Processing    | Apache Spark (Structured Streaming) |
| Notification  | SMTP (Gmail) or AWS SES             |
| Dashboard     | Streamlit                           |
| Storage       | PostgreSQL                          |
| Deployment    | Docker, Docker Compose              |

---

## 🧩 Architecture
```text
            [Weather API] --> [Ingestion Script] --> Kafka (weather_raw)
                                            |
                                    Spark Streaming Job
                                            ↓
                                Stores in PostgreSQL database
                                            ↓
                            Detects Alert Events (storm, heat, etc.)
                                            ↓
                        Kafka (weather_alerts) --> Streamlit Dashboard
                                            ↓
                                Sends Email via SES / SMTP

