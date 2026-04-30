from pydantic import BaseModel, validator
from typing import List

class ContributorRequest(BaseModel):
    name: str
    email: str
    skills: List[str]

    @validator("name")
    def name_length(cls, v):
        if len(v) > 50:
            raise ValueError("Name must be less than 50 characters")
        return v

    @validator("email")
    def email_format(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v

class ProjectRequest(BaseModel):
    name: str
    description: str
    required_skills: List[str]

    @validator("name")
    def name_length(cls, v):
        if len(v) > 50:
            raise ValueError("Name must be less than 50 characters")
        return v

    @validator("description")
    def description_length(cls, v):
        if len(v) > 500:
            raise ValueError("Description must be less than 500 characters")
        return v