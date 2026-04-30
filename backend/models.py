from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import List

Base = declarative_base()

# Many-to-Many relationship table for contributor skills
contributor_skills = Table(
    "contributor_skills",
    Base.metadata,
    Column("contributor_id", Integer, ForeignKey("contributors.id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)

# Many-to-Many relationship table for project required skills
project_required_skills = Table(
    "project_required_skills",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("skill_id", Integer, ForeignKey("skills.id")),
)

# Many-to-Many relationship table for contributor interests
contributor_interests = Table(
    "contributor_interests",
    Base.metadata,
    Column("contributor_id", Integer, ForeignKey("contributors.id")),
    Column("interest_id", Integer, ForeignKey("interests.id")),
)

# Many-to-Many relationship table for project issues
project_issues = Table(
    "project_issues",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("issue_id", Integer, ForeignKey("issues.id")),
)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    skill = Column(String(50), unique=True, nullable=False)

    def __init__(self, skill: str):
        self.skill = skill

class Interest(Base):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True)
    interest = Column(String(50), unique=True, nullable=False)

    def __init__(self, interest: str):
        self.interest = interest

class Contributor(Base):
    __tablename__ = "contributors"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    skills = relationship("Skill", secondary=contributor_skills, backref="contributors")
    interests = relationship("Interest", secondary=contributor_interests, backref="contributors")
    projects = relationship("Project", secondary="contributor_projects", backref="contributors")
    issues = relationship("Issue", secondary="contributor_issues", backref="contributors")
    __table_args__ = (
        Index('ix_contributors_email', 'email'),
    )

    def __init__(self, name: str, email: str, skills: list = None, interests: list = None):
        self.name = name
        self.email = email
        if skills is not None:
            self.skills = skills
        if interests is not None:
            self.interests = interests

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "skills": [skill.skill for skill in self.skills],
            "interests": [interest.interest for interest in self.interests],
        }

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = relationship("Skill", secondary=project_required_skills, backref="projects")
    issues = relationship("Issue", secondary=project_issues, backref="projects")
    contributors = relationship("Contributor", secondary="contributor_projects", backref="projects")

    def __init__(self, name: str, description: str, required_skills: list = None, issues: list = None, contributors: list = None):
        self.name = name
        self.description = description
        if required_skills is not None:
            self.required_skills = required_skills
        if issues is not None:
            self.issues = issues
        if contributors is not None:
            self.contributors = contributors

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "required_skills": [skill.skill for skill in self.required_skills],
        }

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    projects = relationship("Project", secondary=project_issues, backref="issues")
    contributors = relationship("Contributor", secondary="contributor_issues", backref="issues")

    def __init__(self, title: str, description: str, projects: list = None, contributors: list = None):
        self.title = title
        self.description = description
        if projects is not None:
            self.projects = projects
        if contributors is not None:
            self.contributors = contributors

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
        }

# Many-to-Many relationship table for contributor projects
contributor_projects = Table(
    "contributor_projects",
    Base.metadata,
    Column("contributor_id", Integer, ForeignKey("contributors.id")),
    Column("project_id", Integer, ForeignKey("projects.id")),
)

# Many-to-Many relationship table for contributor issues
contributor_issues = Table(
    "contributor_issues",
    Base.metadata,
    Column("contributor_id", Integer, ForeignKey("contributors.id")),
    Column("issue_id", Integer, ForeignKey("issues.id")),
)

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    issue_id = Column(Integer, ForeignKey("issues.id"))
    contributor_id = Column(Integer, ForeignKey("contributors.id"))
    project = relationship("Project", backref="assignments")
    issue = relationship("Issue", backref="assignments")
    contributor = relationship("Contributor", backref="assignments")

    def __init__(self, project_id: int, issue_id: int, contributor_id: int):
        self.project_id = project_id
        self.issue_id = issue_id
        self.contributor_id = contributor_id

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "issue_id": self.issue_id,
            "contributor_id": self.contributor_id,
        }

class ContributionAnalytics(Base):
    __tablename__ = "contribution_analytics"
    id = Column(Integer, primary_key=True)
    contributor_id = Column(Integer, ForeignKey("contributors.id"))
    contributions = Column(Integer, nullable=False)
    projects = Column(Integer, nullable=False)
    issues = Column(Integer, nullable=False)
    contributor = relationship("Contributor", backref="contribution_analytics")

    def __init__(self, contributor_id: int, contributions: int, projects: int, issues: int):
        self.contributor_id = contributor_id
        self.contributions = contributions
        self.projects = projects
        self.issues = issues

    def to_dict(self):
        return {
            "id": self.id,
            "contributor_id": self.contributor_id,
            "contributions": self.contributions,
            "projects": self.projects,
            "issues": self.issues,
        }