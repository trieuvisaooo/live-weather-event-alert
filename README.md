# 🛰️ Real-Time Social Media Sentiment Tracker

A real-time pipeline that ingests tweets and Reddit comments, performs sentiment analysis, and visualizes trending topics and sentiment shifts via an interactive dashboard.

---

## 📌 Project Overview

This project demonstrates how to build an end-to-end data engineering pipeline using real-time data from public APIs (Twitter & Reddit), Apache Kafka for streaming, Spark for processing, and Streamlit for visualization.

### 🔍 Use Cases
- Monitor public sentiment on events, products, or topics
- Detect surges in negative or positive sentiment in real time
- Track trending hashtags and keywords

---

## 🧰 Tech Stack

| Layer             | Tools / Technologies                           |
|-------------------|------------------------------------------------|
| Data Ingestion    | Twitter API v2 (`tweepy`), Reddit API (`praw`) |
| Message Queue     | Apache Kafka                                   |
| Processing Engine | Apache Spark (Structured Streaming, Spark NLP) |
| Storage           | Amazon S3 (for raw & processed data)           |
| Dashboard         | Streamlit                                      |
| CI/CD             | GitHub Actions + Docker                        |
| Deployment        | AWS EC2 or Streamlit Cloud                     |

---