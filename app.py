import os
import socket

import psycopg
from flask import Flask, jsonify

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL")


@app.get("/")
def index():
    return jsonify(
        message="Hello from Docker!",
        host=socket.gethostname(),
        env=os.environ.get("APP_ENV", "dev"),
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/count")
def count():
    if not DATABASE_URL:
        return jsonify(error="DATABASE_URL is not set"), 503
    with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS hits (id SERIAL PRIMARY KEY, ts TIMESTAMPTZ DEFAULT now())")
        conn.execute("INSERT INTO hits DEFAULT VALUES")
        total = conn.execute("SELECT count(*) FROM hits").fetchone()[0]
    return jsonify(hits=total)
# touch
