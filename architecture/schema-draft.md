# Entity Overview
The Open Source Contribution Finder database schema consists of the following entities:
* **Contributors**: represents a contributor with their name, email, and skills
* **Projects**: represents a project with its name, description, and required skills
* **ContributorSkills**: represents the skills of a contributor
* **ProjectSkills**: represents the required skills of a project
* **ContributorProjects**: represents the projects that a contributor is interested in
* **ContributorInterest**: represents the interests of a contributor

# Schema Tables
## Contributors Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY, NOT NULL |
| name | TEXT | NOT NULL |
| email | TEXT | UNIQUE, NOT NULL |
| created_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |
| updated_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |

## Projects Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY, NOT NULL |
| name | TEXT | NOT NULL |
| description | TEXT | NOT NULL |
| created_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |
| updated_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |

## ContributorSkills Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY, NOT NULL |
| contributor_id | INTEGER | FOREIGN KEY(Contributors.id), NOT NULL |
| skill | TEXT | NOT NULL |
| created_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |
| updated_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |

## ProjectSkills Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY, NOT NULL |
| project_id | INTEGER | FOREIGN KEY(Projects.id), NOT NULL |
| skill | TEXT | NOT NULL |
| created_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |
| updated_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |

## ContributorProjects Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY, NOT NULL |
| contributor_id | INTEGER | FOREIGN KEY(Contributors.id), NOT NULL |
| project_id | INTEGER | FOREIGN KEY(Projects.id), NOT NULL |
| created_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |
| updated_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |

## ContributorInterest Table
| Column Name | Data Type | Constraints |
| --- | --- | --- |
| id | INTEGER | PRIMARY KEY, NOT NULL |
| contributor_id | INTEGER | FOREIGN KEY(Contributors.id), NOT NULL |
| interest | TEXT | NOT NULL |
| created_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |
| updated_at | DATE | DEFAULT CURRENT_DATE, NOT NULL |

## Indexes
* Create an index on the `email` column of the `Contributors` table
* Create an index on the `name` column of the `Projects` table
* Create an index on the `contributor_id` column of the `ContributorSkills` table
* Create an index on the `project_id` column of the `ProjectSkills` table
* Create an index on the `contributor_id` column of the `ContributorProjects` table
* Create an index on the `project_id` column of the `ContributorProjects` table

# Relationships
The relationships between the entities are as follows:
* A contributor can have many skills (one-to-many)
* A project can have many required skills (one-to-many)
* A contributor can be interested in many projects (many-to-many)
* A project can have many contributors interested in it (many-to-many)
* A contributor can have many interests (one-to-many)

The ER diagram in text format is as follows:
```
Contributors --*-- ContributorSkills
Contributors --*-- ContributorInterest
Contributors --*-- ContributorProjects
Projects --*-- ProjectSkills
Projects --*-- ContributorProjects
```

# Sample Queries
The following are five common queries that the app will need:
1. Get all contributors with a specific skill:
```sql
SELECT c.* 
FROM Contributors c 
JOIN ContributorSkills cs ON c.id = cs.contributor_id 
WHERE cs.skill = 'Python';
```
2. Get all projects that require a specific skill:
```sql
SELECT p.* 
FROM Projects p 
JOIN ProjectSkills ps ON p.id = ps.project_id 
WHERE ps.skill = 'JavaScript';
```
3. Get all projects that a contributor is interested in:
```sql
SELECT p.* 
FROM Projects p 
JOIN ContributorProjects cp ON p.id = cp.project_id 
WHERE cp.contributor_id = 1;
```
4. Get all contributors who are interested in a specific project:
```sql
SELECT c.* 
FROM Contributors c 
JOIN ContributorProjects cp ON c.id = cp.contributor_id 
WHERE cp.project_id = 1;
```
5. Get all skills of a contributor:
```sql
SELECT cs.skill 
FROM ContributorSkills cs 
WHERE cs.contributor_id = 1;
```

# Migration Notes
The order to create the tables respecting foreign key dependencies is as follows:
1. Create the `Contributors` table
2. Create the `Projects` table
3. Create the `ContributorSkills` table
4. Create the `ProjectSkills` table
5. Create the `ContributorProjects` table
6. Create the `ContributorInterest` table

Note: The above migration order ensures that the tables are created in a way that respects the foreign key dependencies between them.