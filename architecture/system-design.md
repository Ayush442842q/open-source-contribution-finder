# System Design Document: Open Source Contribution Finder
## System Overview
The Open Source Contribution Finder is a web application designed to bridge the gap between open-source contributors and project maintainers. The platform aims to provide a user-friendly interface for contributors to find projects that match their skills, interests, and experience, while also helping project maintainers find suitable contributors for their projects.

### Goals
* Provide a robust search functionality for open-source projects
* Enable contributors to showcase their skills, experience, and interests
* Facilitate collaboration and progress tracking between contributors and project maintainers
* Offer personalized analytics and insights for contributors and maintainers

## Architecture Pattern
The Open Source Contribution Finder will follow a REST API + SPA (Single-Page Application) architecture pattern. The backend will be built using Python and FastAPI, while the frontend will be built using vanilla HTML, CSS, and JavaScript.

## Component Diagram
```markdown
+---------------+
|  Web Client  |
+---------------+
         |
         |
         v
+---------------+
|  Frontend    |
|  (HTML/CSS/JS)|
+---------------+
         |
         |
         v
+---------------+
|  REST API    |
|  (FastAPI)    |
+---------------+
         |
         |
         v
+---------------+
|  Database    |
|  (SQLite)     |
+---------------+
```

## Tech Stack Decision
The following technologies have been chosen for the Open Source Contribution Finder:

* **Backend:** FastAPI (Python) - chosen for its high performance, scalability, and ease of development
* **Frontend:** Vanilla HTML, CSS, and JavaScript - chosen for its simplicity, flexibility, and ease of maintenance
* **Database:** SQLite - chosen for its lightweight, easy-to-use, and self-contained nature

Justification:
* FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
* Vanilla HTML, CSS, and JavaScript are widely adopted and well-understood technologies for building web applications.
* SQLite is a self-contained, file-based database that is easy to set up and maintain, making it an ideal choice for a small to medium-sized application like the Open Source Contribution Finder.

## Directory Structure
The project will follow the following directory structure:
```markdown
open-source-contribution-finder/
|---- app/
|       |---- __init__.py
|       |---- main.py
|       |---- models/
|       |       |---- __init__.py
|       |       |---- contributor.py
|       |       |---- project.py
|       |---- routes/
|       |       |---- __init__.py
|       |       |---- contributors.py
|       |       |---- projects.py
|       |---- schemas/
|       |       |---- __init__.py
|       |       |---- contributor.py
|       |       |---- project.py
|       |---- utils/
|       |       |---- __init__.py
|       |       |---- database.py
|---- frontend/
|       |---- index.html
|       |---- styles.css
|       |---- script.js
|---- database/
|       |---- oscf.db
|---- requirements.txt
|---- README.md
```

## Deployment Strategy
The application will be deployed in the following environments:

* **Local:** The application will be run locally using `uvicorn` for development and testing purposes.
* **Production:** The application will be deployed to a cloud platform (e.g. AWS, Google Cloud) using a containerization tool (e.g. Docker) and an orchestration tool (e.g. Kubernetes).

To run the application locally, navigate to the project directory and run the following command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
To deploy the application to production, follow these steps:

1. Build a Docker image of the application using the following command:
```bash
docker build -t oscc .
```
2. Push the Docker image to a container registry (e.g. Docker Hub).
3. Create a Kubernetes deployment YAML file that defines the deployment configuration.
4. Apply the deployment YAML file to the Kubernetes cluster using the following command:
```bash
kubectl apply -f deployment.yaml
```

## Data Flow
The data will flow through the system as follows:

1. **Contributor Registration:** A contributor registers for the platform by providing their details (e.g. name, email, skills).
2. **Project Creation:** A project maintainer creates a new project by providing its details (e.g. name, description, required skills).
3. **Project Filtering and Search:** A contributor searches for projects that match their skills and interests.
4. **Contributor Profiling and Matching:** The system matches the contributor with suitable projects based on their skills and interests.
5. **Project Issue Tracking and Assignment:** A project maintainer assigns issues to a contributor.
6. **Notification System:** The system sends notifications to the contributor about new project opportunities, updates, and changes.
7. **Personalized Contribution Analytics and Insights:** The system provides personalized analytics and insights to the contributor and project maintainer about their contributions and progress.