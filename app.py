from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Backend is up"
    }), 200

@app.route("/hello", methods=["GET"])
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Hello from Flask!",
            "database": "connected",
            "server_time": str(result[0])
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Hello from Flask!",
            "database": "connection failed",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)