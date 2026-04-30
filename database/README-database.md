# README-database.md
## Database Overview
The database is designed to manage information about contributors, projects, and the skills and interests associated with them. It provides a structured way to store and query data related to contributors' skills, project requirements, and contributor-project assignments.

## Schema Description
The database schema consists of six tables:
- **Contributors**: stores information about individual contributors, including their name, email, and timestamps for creation and update.
- **Projects**: stores information about projects, including their name, description, and timestamps for creation and update.
- **ContributorSkills**: stores the skills associated with each contributor, including the contributor ID, skill name, and timestamps for creation and update.
- **ProjectSkills**: stores the skills required by each project, including the project ID, skill name, and timestamps for creation and update.
- **ContributorProjects**: stores the many-to-many relationship between contributors and projects, including the contributor ID, project ID, and timestamps for creation and update.
- **ContributorInterest**: stores the interests of each contributor, including the contributor ID, interest name, and timestamps for creation and update.

The tables have the following relationships:
- A contributor can have many skills (one-to-many: Contributors -> ContributorSkills).
- A project can have many skills (one-to-many: Projects -> ProjectSkills).
- A contributor can be assigned to many projects (many-to-many: Contributors -> ContributorProjects -> Projects).
- A project can have many contributors (many-to-many: Projects -> ContributorProjects -> Contributors).
- A contributor can have many interests (one-to-many: Contributors -> ContributorInterest).

## Setup Instructions
To set up the database, follow these steps:
1. Install a compatible database management system (e.g., SQLite).
2. Create a new database.
3. Execute the provided SQL script to create the tables and indexes.

## How to Run Migrations
To run migrations, use the following command:
```bash
# assuming you are using a migration tool like Alembic
alembic upgrade head
```
Note: You need to install and configure a migration tool to manage schema changes.

## How to Seed Data
To seed the database with initial data, you can use a data seeding script or a tool like `sqlalchemy` in Python:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create a session
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

# seed data
contributor = Contributor(name='John Doe', email='johndoe@example.com')
session.add(contributor)
session.commit()
```
## Query Examples
Here are some example queries:
- Get all contributors with their skills:
```sql
SELECT c.name, cs.skill
FROM Contributors c
JOIN ContributorSkills cs ON c.id = cs.contributor_id;
```
- Get all projects with their assigned contributors:
```sql
SELECT p.name, c.name
FROM Projects p
JOIN ContributorProjects cp ON p.id = cp.project_id
JOIN Contributors c ON cp.contributor_id = c.id;
```
- Get all contributors with their interests:
```sql
SELECT c.name, ci.interest
FROM Contributors c
JOIN ContributorInterest ci ON c.id = ci.contributor_id;
```
## Index Optimization Notes
The database schema includes indexes on frequently queried columns to improve query performance:
- `idx_contributors_email` on `Contributors.email`
- `idx_projects_name` on `Projects.name`
- `idx_contributor_skills_contributor_id` on `ContributorSkills.contributor_id`
- `idx_project_skills_project_id` on `ProjectSkills.project_id`
- `idx_contributor_projects_contributor_id` on `ContributorProjects.contributor_id`
- `idx_contributor_projects_project_id` on `ContributorProjects.project_id`

Regularly review and optimize indexes to ensure optimal query performance.

## Backup Strategy
To ensure data integrity and availability, implement a regular backup strategy:
- Schedule daily backups of the database using a tool like `cron` or a cloud-based backup service.
- Store backups in a secure, offsite location, such as an external hard drive or cloud storage.
- Test backups regularly to ensure data can be recovered in case of a failure.