# Weather Proxy Service

Production-ready REST API written in Python that acts as a proxy to a public
weather provider, with caching, retries, and basic observability.

## Requirements
- Docker
- Docker Compose

## Run locally

Run the entire environment (API + Redis) with a single command:

```bash
docker-compose up --build

Once running, the service is available at:

- Health check: http://localhost:8000/health
- Weather endpoint: http://localhost:8000/weather?city=Tel%20Aviv

## High-level architecture

- Flask-based REST API
- Redis used as a cache layer
- External weather provider (e.g. Open-Meteo)
- Docker and docker-compose for a production-like local setup

## Design notes

- Redis runs as a separate container and is accessed via Docker’s internal network.
- The API is intentionally kept simple and synchronous.
- The focus is on reliability, clarity, and production best practices rather than feature richness.