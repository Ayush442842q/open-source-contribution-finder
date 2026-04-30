import sqlite3
from datetime import date

# Connect to the SQLite database
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contributors (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE NOT NULL,
        updated_at DATE DEFAULT CURRENT_DATE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE NOT NULL,
        updated_at DATE DEFAULT CURRENT_DATE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ContributorSkills (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contributor_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE NOT NULL,
        updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
        FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProjectSkills (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        project_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE NOT NULL,
        updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
        FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ContributorProjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contributor_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE NOT NULL,
        updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
        FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ContributorInterest (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contributor_id INTEGER NOT NULL,
        interest TEXT NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE NOT NULL,
        updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
        FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
    )
''')

# Create indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_contributors_email ON Contributors (email)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_name ON Projects (name)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_contributor_skills_contributor_id ON ContributorSkills (contributor_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_project_skills_project_id ON ProjectSkills (project_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_contributor_projects_contributor_id ON ContributorProjects (contributor_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_contributor_projects_project_id ON ContributorProjects (project_id)')

# Add CHECK constraints
cursor.execute('ALTER TABLE Contributors ADD CONSTRAINT IF NOT EXISTS chk_contributors_name CHECK (name <> "")')
cursor.execute('ALTER TABLE Contributors ADD CONSTRAINT IF NOT EXISTS chk_contributors_email CHECK (email <> "")')
cursor.execute('ALTER TABLE Projects ADD CONSTRAINT IF NOT EXISTS chk_projects_name CHECK (name <> "")')
cursor.execute('ALTER TABLE Projects ADD CONSTRAINT IF NOT EXISTS chk_projects_description CHECK (description <> "")')
cursor.execute('ALTER TABLE ContributorSkills ADD CONSTRAINT IF NOT EXISTS chk_contributor_skills_skill CHECK (skill <> "")')
cursor.execute('ALTER TABLE ProjectSkills ADD CONSTRAINT IF NOT EXISTS chk_project_skills_skill CHECK (skill <> "")')
cursor.execute('ALTER TABLE ContributorInterest ADD CONSTRAINT IF NOT EXISTS chk_contributor_interest_interest CHECK (interest <> "")')

# Insert seed data
contributors = [
    ('John Doe', 'john@example.com'),
    ('Jane Doe', 'jane@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Alice Johnson', 'alice@example.com'),
    ('Mike Brown', 'mike@example.com')
]

projects = [
    ('Project Alpha', 'A project to test the alpha version of our product'),
    ('Project Beta', 'A project to test the beta version of our product'),
    ('Project Gamma', 'A project to test the gamma version of our product'),
    ('Project Delta', 'A project to test the delta version of our product'),
    ('Project Epsilon', 'A project to test the epsilon version of our product')
]

contributor_skills = [
    (1, 'Python'),
    (1, 'Java'),
    (2, 'JavaScript'),
    (2, 'HTML/CSS'),
    (3, 'C++'),
    (3, 'Ruby'),
    (4, 'Swift'),
    (4, 'Kotlin'),
    (5, 'PHP'),
    (5, 'Go')
]

project_skills = [
    (1, 'Python'),
    (1, 'Java'),
    (2, 'JavaScript'),
    (2, 'HTML/CSS'),
    (3, 'C++'),
    (3, 'Ruby'),
    (4, 'Swift'),
    (4, 'Kotlin'),
    (5, 'PHP'),
    (5, 'Go')
]

contributor_projects = [
    (1, 1),
    (1, 2),
    (2, 2),
    (2, 3),
    (3, 3),
    (3, 4),
    (4, 4),
    (4, 5),
    (5, 5),
    (5, 1)
]

contributor_interests = [
    (1, 'Artificial Intelligence'),
    (1, 'Machine Learning'),
    (2, 'Web Development'),
    (2, 'Data Science'),
    (3, 'Cyber Security'),
    (3, 'Network Security'),
    (4, 'Mobile App Development'),
    (4, 'Game Development'),
    (5, 'Cloud Computing'),
    (5, 'DevOps')
]

cursor.executemany('INSERT INTO Contributors (name, email, created_at, updated_at) VALUES (?, ?, ?, ?)', [(name, email, date.today(), date.today()) for name, email in contributors])
cursor.executemany('INSERT INTO Projects (name, description, created_at, updated_at) VALUES (?, ?, ?, ?)', [(name, description, date.today(), date.today()) for name, description in projects])
cursor.executemany('INSERT INTO ContributorSkills (contributor_id, skill, created_at, updated_at) VALUES (?, ?, ?, ?)', [(contributor_id, skill, date.today(), date.today()) for contributor_id, skill in contributor_skills])
cursor.executemany('INSERT INTO ProjectSkills (project_id, skill, created_at, updated_at) VALUES (?, ?, ?, ?)', [(project_id, skill, date.today(), date.today()) for project_id, skill in project_skills])
cursor.executemany('INSERT INTO ContributorProjects (contributor_id, project_id, created_at, updated_at) VALUES (?, ?, ?, ?)', [(contributor_id, project_id, date.today(), date.today()) for contributor_id, project_id in contributor_projects])
cursor.executemany('INSERT INTO ContributorInterest (contributor_id, interest, created_at, updated_at) VALUES (?, ?, ?, ?)', [(contributor_id, interest, date.today(), date.today()) for contributor_id, interest in contributor_interests])

# Commit changes and close connection
connection.commit()
connection.close()