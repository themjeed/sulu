
from pathlib import Path

def detect_application(project_dir="."):
    project = Path(project_dir)

    print("\n=== APPLICATION DETECTION ===")

    # Detect application type
    if (project / "requirements.txt").exists() or list(project.glob("*.py")):
        app_type = "Python"
    elif (project / "package.json").exists():
        app_type = "Node.js"
    elif (project / "pom.xml").exists():
        app_type = "Java (Maven)"
    elif (project / "build.gradle").exists():
        app_type = "Java (Gradle)"
    elif (project / "composer.json").exists():
        app_type = "PHP"
    elif (project / "go.mod").exists():
        app_type = "Go"
    elif list(project.glob("*.csproj")):
        app_type = ".NET"
    elif (project / "Gemfile").exists():
        app_type = "Ruby"
    else:
        app_type = "Unknown"

    print("Application type:", app_type)

    # Detect dependency files
    dependency_files = [
        "requirements.txt",
        "package.json",
        "pom.xml",
        "build.gradle",
        "composer.json",
        "go.mod",
        "Gemfile"
    ]

    print("\nDependency files:")
    found = False

    for filename in dependency_files:
        if (project / filename).exists():
            print("-", filename)
            found = True

    if not found:
        print("No supported dependency file found")

    # Basic database detection from project configuration
    database_files = {
        "mysql": ["mysql-connector-python", "pymysql", "mysql2"],
        "postgresql": ["psycopg2", "pg", "postgres"],
        "mongodb": ["pymongo", "mongoose", "mongodb"],
        "redis": ["redis"]
    }

    print("\nPossible database dependencies:")

    for database, keywords in database_files.items():
        detected = False

        for filename in dependency_files:
            path = project / filename

            if path.exists():
                content = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()

                if any(keyword in content for keyword in keywords):
                    detected = True

        if detected:
            print("-", database)

if __name__ == "__main__":
    detect_application()
