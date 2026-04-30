import sqlite3
import os

class MigrationScript:
    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name
        self.migration_table = 'migrations'

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_migration_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.migration_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name TEXT NOT NULL,
                applied_at DATE DEFAULT CURRENT_DATE NOT NULL
            );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def apply_migration(self, migration_name, up_query, down_query):
        self.connect()
        self.create_migration_table()

        # Check if migration has already been applied
        query = f"SELECT * FROM {self.migration_table} WHERE name = ?;"
        self.cursor.execute(query, (migration_name,))
        if self.cursor.fetchone():
            print(f"Migration {migration_name} has already been applied. Skipping...")
            return

        try:
            # Apply the migration
            self.cursor.executescript(up_query)
            self.conn.commit()
            # Log the migration
            query = f"INSERT INTO {self.migration_table} (name) VALUES (?);"
            self.cursor.execute(query, (migration_name,))
            self.conn.commit()
            print(f"Migration {migration_name} applied successfully.")
        except sqlite3.Error as e:
            # Rollback the migration if it fails
            self.cursor.executescript(down_query)
            self.conn.commit()
            print(f"Error applying migration {migration_name}: {e}")

    def rollback_migration(self, migration_name, down_query):
        self.connect()

        # Check if migration has been applied
        query = f"SELECT * FROM {self.migration_table} WHERE name = ?;"
        self.cursor.execute(query, (migration_name,))
        if not self.cursor.fetchone():
            print(f"Migration {migration_name} has not been applied. Skipping...")
            return

        try:
            # Rollback the migration
            self.cursor.executescript(down_query)
            self.conn.commit()
            # Remove the migration log
            query = f"DELETE FROM {self.migration_table} WHERE name = ?;"
            self.cursor.execute(query, (migration_name,))
            self.conn.commit()
            print(f"Migration {migration_name} rolled back successfully.")
        except sqlite3.Error as e:
            print(f"Error rolling back migration {migration_name}: {e}")

def main():
    db_name = 'contributors.db'
    migration_script = MigrationScript(db_name)

    # Migration 1: Create tables
    migration_name = 'create_tables'
    up_query = """
        -- Create the Contributors table
        CREATE TABLE IF NOT EXISTS Contributors (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL
        );

        -- Create the Projects table
        CREATE TABLE IF NOT EXISTS Projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL
        );

        -- Create the ContributorSkills table
        CREATE TABLE IF NOT EXISTS ContributorSkills (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contributor_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
        );

        -- Create the ProjectSkills table
        CREATE TABLE IF NOT EXISTS ProjectSkills (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            project_id INTEGER NOT NULL,
            skill TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
        );

        -- Create the ContributorProjects table
        CREATE TABLE IF NOT EXISTS ContributorProjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contributor_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
        );

        -- Create the ContributorInterest table
        CREATE TABLE IF NOT EXISTS ContributorInterest (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contributor_id INTEGER NOT NULL,
            interest TEXT NOT NULL,
            created_at DATE DEFAULT CURRENT_DATE NOT NULL,
            updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
            FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
        );

        -- Create indexes for frequently queried columns
        CREATE INDEX IF NOT EXISTS idx_contributors_email ON Contributors (email);
        CREATE INDEX IF NOT EXISTS idx_projects_name ON Projects (name);
        CREATE INDEX IF NOT EXISTS idx_contributor_skills_contributor_id ON ContributorSkills (contributor_id);
        CREATE INDEX IF NOT EXISTS idx_project_skills_project_id ON ProjectSkills (project_id);
        CREATE INDEX IF NOT EXISTS idx_contributor_projects_contributor_id ON ContributorProjects (contributor_id);
        CREATE INDEX IF NOT EXISTS idx_contributor_projects_project_id ON ContributorProjects (project_id);
    """
    down_query = """
        DROP TABLE IF EXISTS ContributorInterest;
        DROP TABLE IF EXISTS ContributorProjects;
        DROP TABLE IF EXISTS ProjectSkills;
        DROP TABLE IF EXISTS ContributorSkills;
        DROP TABLE IF EXISTS Projects;
        DROP TABLE IF EXISTS Contributors;
    """

    migration_script.apply_migration(migration_name, up_query, down_query)

    # Migration 2: Add CHECK constraints
    migration_name = 'add_check_constraints'
    up_query = """
        -- Add CHECK constraints for validation
        ALTER TABLE Contributors ADD CONSTRAINT IF NOT EXISTS chk_contributors_name CHECK (name <> '');
        ALTER TABLE Contributors ADD CONSTRAINT IF NOT EXISTS chk_contributors_email CHECK (email <> '');
        ALTER TABLE Projects ADD CONSTRAINT IF NOT EXISTS chk_projects_name CHECK (name <> '');
        ALTER TABLE Projects ADD CONSTRAINT IF NOT EXISTS chk_projects_description CHECK (description <> '');
        ALTER TABLE ContributorSkills ADD CONSTRAINT IF NOT EXISTS chk_contributor_skills_skill CHECK (skill <> '');
        ALTER TABLE ProjectSkills ADD CONSTRAINT IF NOT EXISTS chk_project_skills_skill CHECK (skill <> '');
        ALTER TABLE ContributorInterest ADD CONSTRAINT IF NOT EXISTS chk_contributor_interest_interest CHECK (interest <> '');
    """
    down_query = """
        -- Remove CHECK constraints
        ALTER TABLE Contributors DROP CONSTRAINT IF EXISTS chk_contributors_name;
        ALTER TABLE Contributors DROP CONSTRAINT IF EXISTS chk_contributors_email;
        ALTER TABLE Projects DROP CONSTRAINT IF EXISTS chk_projects_name;
        ALTER TABLE Projects DROP CONSTRAINT IF EXISTS chk_projects_description;
        ALTER TABLE ContributorSkills DROP CONSTRAINT IF EXISTS chk_contributor_skills_skill;
        ALTER TABLE ProjectSkills DROP CONSTRAINT IF EXISTS chk_project_skills_skill;
        ALTER TABLE ContributorInterest DROP CONSTRAINT IF EXISTS chk_contributor_interest_interest;
    """

    migration_script.apply_migration(migration_name, up_query, down_query)

if __name__ == '__main__':
    main()
migration_script.rollback_migration('create_tables', down_query)