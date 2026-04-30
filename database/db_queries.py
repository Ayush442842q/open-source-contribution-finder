import sqlite3
from sqlite3 import Error
from typing import List, Tuple

class Database:
    def __init__(self, db_file: str):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            print(f"Connected to SQLite Database {db_file}")
        except Error as e:
            print(e)

    def create_tables(self):
        # Create Contributors table
        contributors_table = """CREATE TABLE IF NOT EXISTS Contributors (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL
        );"""
        self.execute_query(contributors_table)

        # Create Projects table
        projects_table = """CREATE TABLE IF NOT EXISTS Projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL
        );"""
        self.execute_query(projects_table)

        # Create ContributorSkills table
        contributor_skills_table = """CREATE TABLE IF NOT EXISTS ContributorSkills (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contributor_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
        );"""
        self.execute_query(contributor_skills_table)

        # Create ProjectSkills table
        project_skills_table = """CREATE TABLE IF NOT EXISTS ProjectSkills (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            project_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
        );"""
        self.execute_query(project_skills_table)

        # Create ContributorProjects table
        contributor_projects_table = """CREATE TABLE IF NOT EXISTS ContributorProjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contributor_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
        );"""
        self.execute_query(contributor_projects_table)

        # Create ContributorInterest table
        contributor_interest_table = """CREATE TABLE IF NOT EXISTS ContributorInterest (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contributor_id INTEGER NOT NULL,
            interest TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
        );"""
        self.execute_query(contributor_interest_table)

    def execute_query(self, query: str):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except Error as e:
            print(e)

    def create_contributor(self, name: str, email: str) -> Tuple[int, str, str]:
        query = """INSERT INTO Contributors (name, email) VALUES (?, ?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (name, email))
            self.conn.commit()
            contributor_id = cursor.lastrowid
            return contributor_id, name, email
        except Error as e:
            print(e)
            return None

    def get_contributor(self, contributor_id: int) -> Tuple[int, str, str]:
        query = """SELECT id, name, email FROM Contributors WHERE id = ?"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (contributor_id,))
            row = cursor.fetchone()
            if row:
                return row[0], row[1], row[2]
            else:
                return None
        except Error as e:
            print(e)
            return None

    def create_project(self, name: str, description: str) -> Tuple[int, str, str]:
        query = """INSERT INTO Projects (name, description) VALUES (?, ?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (name, description))
            self.conn.commit()
            project_id = cursor.lastrowid
            return project_id, name, description
        except Error as e:
            print(e)
            return None

    def get_project(self, project_id: int) -> Tuple[int, str, str]:
        query = """SELECT id, name, description FROM Projects WHERE id = ?"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (project_id,))
            row = cursor.fetchone()
            if row:
                return row[0], row[1], row[2]
            else:
                return None
        except Error as e:
            print(e)
            return None

    def create_contributor_skill(self, contributor_id: int, skill: str) -> Tuple[int, int, str]:
        query = """INSERT INTO ContributorSkills (contributor_id, skill) VALUES (?, ?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (contributor_id, skill))
            self.conn.commit()
            contributor_skill_id = cursor.lastrowid
            return contributor_skill_id, contributor_id, skill
        except Error as e:
            print(e)
            return None

    def create_project_skill(self, project_id: int, skill: str) -> Tuple[int, int, str]:
        query = """INSERT INTO ProjectSkills (project_id, skill) VALUES (?, ?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (project_id, skill))
            self.conn.commit()
            project_skill_id = cursor.lastrowid
            return project_skill_id, project_id, skill
        except Error as e:
            print(e)
            return None

    def create_contributor_project(self, contributor_id: int, project_id: int) -> Tuple[int, int, int]:
        query = """INSERT INTO ContributorProjects (contributor_id, project_id) VALUES (?, ?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (contributor_id, project_id))
            self.conn.commit()
            contributor_project_id = cursor.lastrowid
            return contributor_project_id, contributor_id, project_id
        except Error as e:
            print(e)
            return None

    def create_contributor_interest(self, contributor_id: int, interest: str) -> Tuple[int, int, str]:
        query = """INSERT INTO ContributorInterest (contributor_id, interest) VALUES (?, ?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (contributor_id, interest))
            self.conn.commit()
            contributor_interest_id = cursor.lastrowid
            return contributor_interest_id, contributor_id, interest
        except Error as e:
            print(e)
            return None

    def search_projects(self, skills: List[str], interests: List[str]) -> List[Tuple[int, str, str]]:
        query = """SELECT p.id, p.name, p.description 
                  FROM Projects p 
                  JOIN ProjectSkills ps ON p.id = ps.project_id 
                  JOIN ContributorProjects cp ON p.id = cp.project_id 
                  JOIN Contributors c ON cp.contributor_id = c.id 
                  JOIN ContributorSkills cs ON c.id = cs.contributor_id 
                  JOIN ContributorInterest ci ON c.id = ci.contributor_id 
                  WHERE ps.skill IN (?) AND ci.interest IN (?)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, (",".join(skills), ",".join(interests)))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print(e)
            return None

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

# Example usage:
if __name__ == "__main__":
    db = Database("oscf.db")
    db.create_tables()

    # Create contributor
    contributor_id, name, email = db.create_contributor("John Doe", "john.doe@example.com")
    print(f"Contributor created: {contributor_id}, {name}, {email}")

    # Create project
    project_id, name, description = db.create_project("Example Project", "This is an example project")
    print(f"Project created: {project_id}, {name}, {description}")

    # Create contributor skill
    contributor_skill_id, contributor_id, skill = db.create_contributor_skill(contributor_id, "Python")
    print(f"Contributor skill created: {contributor_skill_id}, {contributor_id}, {skill}")

    # Create project skill
    project_skill_id, project_id, skill = db.create_project_skill(project_id, "JavaScript")
    print(f"Project skill created: {project_skill_id}, {project_id}, {skill}")

    # Create contributor project
    contributor_project_id, contributor_id, project_id = db.create_contributor_project(contributor_id, project_id)
    print(f"Contributor project created: {contributor_project_id}, {contributor_id}, {project_id}")

    # Create contributor interest
    contributor_interest_id, contributor_id, interest = db.create_contributor_interest(contributor_id, "web development")
    print(f"Contributor interest created: {contributor_interest_id}, {contributor_id}, {interest}")

    # Search projects
    skills = ["Python", "JavaScript"]
    interests = ["web development"]
    projects = db.search_projects(skills, interests)
    print(f"Search projects: {projects}")

    db.close_connection()