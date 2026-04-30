from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from logging.config import dictConfig
import os
import logging
from fastapi import Request

# Logging configuration
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})

# Database configuration
SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class Contributor(Base):
    __tablename__ = 'contributors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    skills = Column(String)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    required_skills = Column(String)

# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI application
app = FastAPI()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT secret key
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))

# CORS configuration
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://api.oscf.com",
    "https://app.oscf.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT token generation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT token verification
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logging.error(f"JWT token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Login endpoint
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace this with your actual authentication logic
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Replace this with your actual user retrieval logic
        user = {"username": username}
        return user
    except JWTError as e:
        logging.error(f"JWT token verification error: {e}")
        raise credentials_exception

class ContributorModel(BaseModel):
    name: str
    email: str
    skills: str

class ProjectModel(BaseModel):
    name: str
    description: str
    required_skills: list[str]

class ContributorEmailModel(BaseModel):
    email: EmailStr

# Register contributor endpoint
@app.post("/contributors")
async def register_contributor(contributor: ContributorModel, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        existing_contributor = db.query(Contributor).filter(Contributor.email == contributor.email).first()
        if existing_contributor:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Contributor already exists"
            )
        new_contributor = Contributor(name=contributor.name, email=contributor.email, skills=contributor.skills)
        db.add(new_contributor)
        db.commit()
        db.close()
        return {"id": new_contributor.id, "name": new_contributor.name, "email": new_contributor.email, "skills": new_contributor.skills}
    except Exception as e:
        db = SessionLocal()
        db.rollback()
        db.close()
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register contributor"
        )

# Get contributor profile endpoint
@app.get("/contributors/{contributor_id}")
async def get_contributor_profile(contributor_id: int, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        contributor = db.query(Contributor).filter(Contributor.id == contributor_id).first()
        if not contributor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contributor not found"
            )
        contributor_email = ContributorEmailModel(email=contributor.email)
        db.close()
        return {"id": contributor.id, "name": contributor.name, "email": contributor_email.email, "skills": contributor.skills}
    except Exception as e:
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve contributor profile"
        )

# Create project endpoint
@app.post("/projects")
async def create_project(project: ProjectModel, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        existing_project = db.query(Project).filter(Project.name == project.name).first()
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Project already exists"
            )
        required_skills = ",".join(project.required_skills)
        new_project = Project(name=project.name, description=project.description, required_skills=required_skills)
        db.add(new_project)
        db.commit()
        db.close()
        return {"id": new_project.id, "name": new_project.name, "description": new_project.description, "requiredSkills": project.required_skills}
    except Exception as e:
        db = SessionLocal()
        db.rollback()
        db.close()
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )

# Get project endpoint
@app.get("/projects/{project_id}")
async def get_project(project_id: int, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        required_skills = project.required_skills.split(",") if project.required_skills else []
        db.close()
        return {"id": project.id, "name": project.name, "description": project.description, "requiredSkills": required_skills}
    except Exception as e:
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project"
        )

# Search projects endpoint
@app.get("/projects")
async def search_projects(skills: str = None, interests: str = None, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        projects = db.query(Project).all()
        if skills:
            projects = [project for project in projects if any(skill in project.required_skills for skill in skills.split(','))]
        if interests:
            projects = [project for project in projects if any(interest in project.description for interest in interests.split(','))]
        db.close()
        return [{"id": project.id, "name": project.name, "description": project.description, "requiredSkills": project.required_skills.split(",") if project.required_skills else []} for project in projects]
    except Exception as e:
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search projects"
        )

# Assign issue endpoint
@app.post("/projects/{project_id}/issues/{issue_id}/assign")
async def assign_issue(project_id: int, issue_id: int, contributor_id: int, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        # Replace this with your actual issue retrieval logic
        issue = {"id": issue_id}
        contributor = db.query(Contributor).filter(Contributor.id == contributor_id).first()
        if not contributor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contributor not found"
            )
        db.close()
        return {"id": issue['id'], "projectId": project_id, "issueId": issue_id, "contributorId": contributor_id}
    except Exception as e:
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign issue"
        )

# Get contribution analytics endpoint
@app.get("/contributors/{contributor_id}/analytics")
async def get_contribution_analytics(contributor_id: int, current_user: dict = Depends(get_current_user)):
    try:
        db = SessionLocal()
        contributor = db.query(Contributor).filter(Contributor.id == contributor_id).first()
        if not contributor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contributor not found"
            )
        # Replace this with your actual analytics retrieval logic
        analytics = {"contributions": 10, "projects": 5, "issues": 20}
        db.close()
        return analytics
    except Exception as e:
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve contribution analytics"
        )

# Error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except JWTError as e:
        logging.error(f"JWT token verification error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logging.error(e)
        logging.critical(f"Critical error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Rate limiting middleware
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    # Replace this with your actual rate limiting logic
    if request.method == "GET":
        return await call_next(request)
    if request.method == "POST":
        if request.headers.get("X-Forwarded-For"):
            ip_address = request.headers.get("X-Forwarded-For")
        else:
            ip_address = request.client.host
        # Check if the IP address has made more than 100 requests in the last minute
        if True:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests"
            )
        return await call_next(request)
    return await call_next(request)