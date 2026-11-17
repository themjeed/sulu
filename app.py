
from flask import Flask
import os
import mysql.connector

app = Flask(__name__)

@app.route("/")
def home():
    return "Updated success! Jenkins and Docker automation is working!"

@app.route("/db")
def database():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "appuser"),
            password=os.getenv("DB_PASSWORD", "apppass"),
            database=os.getenv("DB_NAME", "appdb")
        )
        conn.close()
        return "MySQL database connected successfully!"
    except Exception as e:
        return f"Database connection failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
