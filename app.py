from flask import Flask, jsonify
import os
import psycopg2
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing environment variable: {name}")
    return value


def get_secret_client() -> SecretClient:
    vault_url = get_required_env("keyvaulturl")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)


def get_secret_value(secret_name: str) -> str:
    client = get_secret_client()
    return client.get_secret(secret_name).value


def get_db_connection():
    db_host = get_secret_value("url")
    db_user = get_secret_value("username")
    db_password = get_secret_value("password")

    return psycopg2.connect(
        host=db_host,
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "postgres"),
        user=db_user,
        password=db_password,
        sslmode="require",
    )


@app.route("/", methods=["GET"])
def home():
    return (
        jsonify(
            {
                "success": True,
                "endpoint": "/",
                "message": "Backend is running - KEYVAULT VERSION",
            }
        ),
        200,
    )


@app.route("/hello", methods=["GET"])
def hello():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()

        return (
            jsonify(
                {
                    "success": True,
                    "endpoint": "/hello",
                    "message": "Hello from Flask with Key Vault!",
                    "database_status": "connected",
                    "server_time": str(result[0]),
                    "version": "keyvault-v1",
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "endpoint": "/hello",
                    "message": "Key Vault or database connection failed",
                    "error": str(e),
                    "version": "keyvault-v1",
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
