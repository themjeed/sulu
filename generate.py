
from pathlib import Path

project = Path(".")

# Read dependency information
requirements = project / "requirements.txt"

if not requirements.exists():
    raise SystemExit("ERROR: requirements.txt not found")

content = requirements.read_text(
    encoding="utf-8",
    errors="ignore"
).lower()

# Detect database
database = None

if any(x in content for x in [
    "mysql-connector-python", "pymysql", "mysql2"
]):
    database = "mysql"
elif any(x in content for x in [
    "psycopg2", "psycopg", "postgres"
]):
    database = "postgres"
elif any(x in content for x in [
    "pymongo", "mongoengine", "mongoose"
]):
    database = "mongodb"
elif "redis" in content:
    database = "redis"

# Generate Dockerfile
dockerfile = """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
"""

Path("Dockerfile.generated").write_text(
    dockerfile, encoding="utf-8"
)

# Generate Docker Compose
if database == "mysql":
    compose = """services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.generated
    ports:
      - "5002:5000"
    environment:
      DB_HOST: db
      DB_USER: appuser
      DB_PASSWORD: apppass
      DB_NAME: appdb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: appdb
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppass
    volumes:
      - generated_mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-prootpass"]
      interval: 10s
      timeout: 5s
      retries: 10

volumes:
  generated_mysql_data:
"""
elif database is None:
    compose = """services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.generated
    ports:
      - "5002:5000"
"""
else:
    raise SystemExit(
        f"Database '{database}' detected, but its Compose template "
        "has not been implemented yet."
    )

Path("docker-compose.generated.yml").write_text(
    compose, encoding="utf-8"
)

print("=== GENERATION COMPLETE ===")
print("Application: Python")
print("Database:", database or "No database detected")
print("Created: Dockerfile.generated")
print("Created: docker-compose.generated.yml")
