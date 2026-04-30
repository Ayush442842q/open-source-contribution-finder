# Open Source Contribution Finder
A platform that bridges the gap between open-source contributors and project maintainers.

[![Build Status](https://img.shields.io/travis/com/github/OpenSourceContributionFinder.svg?label=Build)](https://travis-ci.com/github/OpenSourceContributionFinder)
[![License](https://img.shields.io/github/license/OpenSourceContributionFinder.svg?label=License)](https://github.com/OpenSourceContributionFinder/blob/main/LICENSE)
[![Version](https://img.shields.io/github/v/release/OpenSourceContributionFinder.svg?label=Version)](https://github.com/OpenSourceContributionFinder/releases)

## Description
The Open Source Contribution Finder is a web application designed to streamline the process of finding and contributing to open-source projects. This platform enables developers to find projects that match their skills, interests, and experience, while also helping project maintainers find suitable contributors for their projects. By leveraging a user-friendly interface and robust matching algorithm, the Open Source Contribution Finder aims to increase the efficiency and effectiveness of open-source contributions.

The platform provides valuable insights and analytics to help contributors and maintainers track their progress and make data-driven decisions. With the increasing popularity of open-source software, there is a high demand for a platform that streamlines the contribution process, making it easier for developers to get involved and for maintainers to find the right contributors.

## Features
* **Project Filtering and Search**: A robust search functionality that allows users to filter open-source projects based on programming languages, project topics, and required skills.
* **Contributor Profiling and Matching**: A user profiling system that enables contributors to showcase their skills, experience, and interests, and matches them with suitable open-source projects.
* **Project Issue Tracking and Assignment**: A feature that allows project maintainers to track and assign issues to contributors, facilitating collaboration and progress tracking.
* **Notification System**: A notification system that alerts contributors to new project opportunities, updates, and changes, ensuring they stay informed and engaged.
* **Personalized Contribution Analytics and Insights**: A dashboard that provides contributors and maintainers with personalized analytics and insights on their contributions, helping them track their progress and identify areas for improvement.

## Tech Stack
The Open Source Contribution Finder is built using a combination of technologies, including:
* **Backend**: FastAPI (Python) for building a high-performance REST API.
* **Frontend**: Vanilla HTML, CSS, and JavaScript for creating a simple and maintainable user interface.
* **Database**: SQLite for storing and managing data in a lightweight and self-contained manner.

## Architecture Overview
The platform follows a REST API + SPA (Single-Page Application) architecture pattern, with the backend built using FastAPI and the frontend built using vanilla HTML, CSS, and JavaScript. The component diagram is as follows:
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
## Getting Started
### Prerequisites
* Python 3.7+
* FastAPI
* SQLite

### Installation
1. Clone the repository: `git clone https://github.com/OpenSourceContributionFinder.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the database: `python init_db.py`

### Environment Variables
| Name | Description | Required/Optional |
| --- | --- | --- |
| `DATABASE_URL` | Database connection URL | Required |
| `SECRET_KEY` | Secret key for JWT authentication | Required |
| `DEBUG` | Enable debug mode | Optional |

### Running Locally
1. Start the backend: `uvicorn main:app --host 0.0.0.0 --port 8000`
2. Start the frontend: `npm start` (if using a frontend framework)

## API Documentation
The API documentation can be found at [https://api.oscf.com/v1/docs](https://api.oscf.com/v1/docs). The API uses a versioning strategy to ensure backwards compatibility. The base URL for the API is `https://api.oscf.com/v1`.

### Endpoints
* `POST /api/v1/contributors`: Registers a new contributor.
* `GET /api/v1/contributors/{id}`: Retrieves a contributor's profile.
* `POST /api/v1/projects`: Creates a new project.
* `GET /api/v1/projects/{id}`: Retrieves a project's details.

## Database Schema
The database schema is designed to store information about contributors, projects, and issues. The schema is as follows:
```sql
CREATE TABLE contributors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    skills TEXT NOT NULL
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT NOT NULL
);

CREATE TABLE issues (
    id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```
## Project Structure
The project structure is as follows:
```markdown
OpenSourceContributionFinder/
|-- app/
|   |-- main.py
|   |-- models/
|   |   |-- contributor.py
|   |   |-- project.py
|   |   |-- issue.py
|   |-- routes/
|   |   |-- contributors.py
|   |   |-- projects.py
|   |   |-- issues.py
|-- frontend/
|   |-- index.html
|   |-- styles.css
|   |-- script.js
|-- database/
|   |-- init_db.py
|   |-- schema.sql
|-- requirements.txt
|-- README.md
```
## Contributing
Contributions are welcome! Please submit a pull request with your changes and a brief description of what you've done.

## License
The Open Source Contribution Finder is licensed under the MIT License.

## Credits
Built by autonomous pipeline.