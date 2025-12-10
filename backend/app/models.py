from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union

class PersonalInfo(BaseModel):
    name: str
    email: Union[EmailStr, None] = None
    phone: Union[str, None] = None
    location: Union[str, None] = None
    linkedin: Union[str, None] = None
    github: Union[str, None] = None
    website: Union[str, None] = None

class Experience(BaseModel):
    company: str
    position: str
    start_date: Union[str, None] = None
    end_date: Union[str, None] = None
    description: Union[str, None] = None
    responsibilities: List[str] = []

class Education(BaseModel):
    institution: str
    degree: str
    field: Union[str, None] = None
    start_date: Union[str, None] = None
    end_date: Union[str, None] = None
    gpa: Union[str, None] = None

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    link: Union[str, None] = None
    github: Union[str, None] = None

class PortfolioData(BaseModel):
    personal_info: PersonalInfo
    summary: Union[str, None] = None
    experience: List[Experience] = []
    education: List[Education] = []
    skills: List[str] = []
    projects: List[Project] = []
    certifications: List[str] = []

class TextPromptRequest(BaseModel):
    prompt: str

class PortfolioGenerateRequest(BaseModel):
    data: PortfolioData
    template: str = "template1"