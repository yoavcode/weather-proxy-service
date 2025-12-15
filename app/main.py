import os
import redis

from flask import Flask, jsonify

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True,
)

@app.route("/health", methods=["GET"])
def health():
    try:
        redis_client.ping()
        redis_status = "up"
    except redis.RedisError:
        redis_status = "down"

    return jsonify({
        "status": "ok",
        "redis": redis_status,
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
