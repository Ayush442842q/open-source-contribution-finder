-- Drop existing tables to ensure a clean start
DROP TABLE IF EXISTS Contributors;
DROP TABLE IF EXISTS Projects;
DROP TABLE IF EXISTS ContributorSkills;
DROP TABLE IF EXISTS ProjectSkills;
DROP TABLE IF EXISTS ContributorProjects;
DROP TABLE IF EXISTS ContributorInterest;

-- Create the Contributors table
CREATE TABLE Contributors (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    updated_at DATE DEFAULT CURRENT_DATE NOT NULL
);

-- Create the Projects table
CREATE TABLE Projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    updated_at DATE DEFAULT CURRENT_DATE NOT NULL
);

-- Create the ContributorSkills table
CREATE TABLE ContributorSkills (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    contributor_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
    FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the ProjectSkills table
CREATE TABLE ProjectSkills (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    project_id INTEGER NOT NULL,
    skill TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the ContributorProjects table
CREATE TABLE ContributorProjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    contributor_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
    FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (project_id) REFERENCES Projects (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the ContributorInterest table
CREATE TABLE ContributorInterest (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    contributor_id INTEGER NOT NULL,
    interest TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    updated_at DATE DEFAULT CURRENT_DATE NOT NULL,
    FOREIGN KEY (contributor_id) REFERENCES Contributors (id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create indexes for frequently queried columns
CREATE INDEX idx_contributors_email ON Contributors (email);
CREATE INDEX idx_projects_name ON Projects (name);
CREATE INDEX idx_contributor_skills_contributor_id ON ContributorSkills (contributor_id);
CREATE INDEX idx_project_skills_project_id ON ProjectSkills (project_id);
CREATE INDEX idx_contributor_projects_contributor_id ON ContributorProjects (contributor_id);
CREATE INDEX idx_contributor_projects_project_id ON ContributorProjects (project_id);

-- Add CHECK constraints for validation
ALTER TABLE Contributors ADD CONSTRAINT chk_contributors_name CHECK (name <> '');
ALTER TABLE Contributors ADD CONSTRAINT chk_contributors_email CHECK (email <> '');
ALTER TABLE Projects ADD CONSTRAINT chk_projects_name CHECK (name <> '');
ALTER TABLE Projects ADD CONSTRAINT chk_projects_description CHECK (description <> '');
ALTER TABLE ContributorSkills ADD CONSTRAINT chk_contributor_skills_skill CHECK (skill <> '');
ALTER TABLE ProjectSkills ADD CONSTRAINT chk_project_skills_skill CHECK (skill <> '');
ALTER TABLE ContributorInterest ADD CONSTRAINT chk_contributor_interest_interest CHECK (interest <> '');