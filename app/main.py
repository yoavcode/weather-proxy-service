import os
import redis
import uuid
import json
import logging
import time

from flask import Flask, jsonify, request, g

app = Flask(__name__)

logger = logging.getLogger("weather-proxy")
logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.WARNING)


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True,
)


@app.before_request
def assign_request_id():
    rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    g.request_id = rid


@app.before_request
def start_timer():
    g.start_time = time.monotonic()


@app.after_request
def add_request_id_header_and_log(response):
    response.headers["X-Request-ID"] = g.request_id

    duration_ms = int((time.monotonic() - g.start_time) * 1000)
    log_event = {
        "request_id": g.request_id,
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    }
    logger.info(json.dumps(log_event))

    return response


@app.route("/health", methods=["GET"])
def health():
    try:
        redis_client.ping()
        redis_status = "up"
    except redis.RedisError:
        redis_status = "down"

    return (
        jsonify(
            {
                "status": "ok",
                "redis": redis_status,
            }
        ),
        200,
    )


@app.route("/weather", methods=["GET"])
def weather():
    city = (request.args.get("city") or "").strip()
    if not city:
        return jsonify({"error": "city query param is required"}), 400
    return jsonify({"city": city, "status": "not implemented yet"}), 501


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
