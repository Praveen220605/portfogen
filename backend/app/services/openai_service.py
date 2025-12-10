from openai import OpenAI
from app.config import settings
from app.models import PortfolioData
import json

class OpenAIService:
    """
    Handles all OpenAI API interactions for portfolio data extraction
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    def extract_portfolio_data(self, resume_text: str) -> PortfolioData:
        """Extract structured data from resume text using AI"""
        
        system_prompt = """You are an expert resume parser. Extract information from the resume text and return it in the following JSON format:

{
  "personal_info": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "+1234567890",
    "location": "City, Country",
    "linkedin": "linkedin.com/in/username",
    "github": "github.com/username",
    "website": "website.com"
  },
  "summary": "Professional summary or objective",
  "experience": [
    {
      "company": "Company Name",
      "position": "Job Title",
      "start_date": "Jan 2020",
      "end_date": "Present",
      "description": "Brief description",
      "responsibilities": ["Point 1", "Point 2"]
    }
  ],
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Science",
      "field": "Computer Science",
      "start_date": "2016",
      "end_date": "2020",
      "gpa": "3.8/4.0"
    }
  ],
  "skills": ["Python", "JavaScript", "React"],
  "projects": [
    {
      "name": "Project Name",
      "description": "What the project does",
      "technologies": ["Tech1", "Tech2"],
      "link": "project-url.com",
      "github": "github.com/user/repo"
    }
  ],
  "certifications": ["Certification 1", "Certification 2"]
}

Extract as much information as possible. If information is missing, use null or empty arrays. Return ONLY valid JSON, no additional text."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Resume text:\n\n{resume_text}"}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data_dict = json.loads(content)
            portfolio_data = PortfolioData(**data_dict)
            
            return portfolio_data
        
        except Exception as e:
            raise Exception(f"Error extracting portfolio data: {str(e)}")
    
    def extract_from_prompt(self, prompt: str) -> PortfolioData:
        """Extract portfolio data from user's text description"""
        
        system_prompt = """You are helping create a portfolio website. Based on the user's description, generate portfolio data in JSON format following this structure:

{
  "personal_info": {...},
  "summary": "...",
  "experience": [...],
  "education": [...],
  "skills": [...],
  "projects": [...],
  "certifications": [...]
}

Be creative and fill in reasonable details based on the description. Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data_dict = json.loads(content)
            portfolio_data = PortfolioData(**data_dict)
            
            return portfolio_data
        
        except Exception as e:
            raise Exception(f"Error processing prompt: {str(e)}")
    
    def refine_portfolio(self, current_data: PortfolioData, refinement_request: str) -> PortfolioData:
        """Refine existing portfolio based on user feedback"""
        
        system_prompt = """You are refining a portfolio website. The user has requested changes. Update the portfolio data accordingly and return the complete updated JSON."""

        try:
            current_json = current_data.model_dump_json()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Current data:\n{current_json}\n\nUser request: {refinement_request}"}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data_dict = json.loads(content)
            portfolio_data = PortfolioData(**data_dict)
            
            return portfolio_data
        
        except Exception as e:
            raise Exception(f"Error refining portfolio: {str(e)}")