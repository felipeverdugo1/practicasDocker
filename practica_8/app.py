import os
import socket
import time

import psycopg2
import redis
from flask import Flask, jsonify

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
REDIS_URL = os.environ.get("REDIS_URL")

r = redis.from_url(REDIS_URL)


def get_db_connection(retries=5, delay=2):
    """Reintenta conectar a Postgres. Útil para ver qué pasa
    cuando la DB tarda en levantar o se cae."""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            return conn
        except psycopg2.OperationalError as e:
            last_error = e
            print(f"[intento {attempt}] no pude conectar a la DB: {e}")
            time.sleep(delay)
    raise last_error


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, ts TIMESTAMP DEFAULT NOW())"
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/api/hello")
def hello():
    # contador rápido en redis (para ver caché / estado compartido entre replicas)
    total = r.incr("hits")

    # guardamos un registro persistente en postgres
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM visits")
    db_rows = cur.fetchone()[0]
    cur.close()
    conn.close()

    return jsonify(
        {
            "mensaje": "hola desde el backend",
            "hostname_contenedor": socket.gethostname(),
            "hits_redis": total,
            "filas_en_postgres": db_rows,
        }
    )


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "hostname": socket.gethostname()})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
