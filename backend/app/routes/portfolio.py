from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.models import (
    PortfolioData, 
    TextPromptRequest, 
    PortfolioGenerateRequest
)
from app.services.nlp_extractor import NLPExtractor
from app.services.portfolio_generator import PortfolioGenerator

router = APIRouter()

# Initialize services
nlp_extractor = NLPExtractor()
portfolio_generator = PortfolioGenerator()

# Request model for refine endpoint
class RefineRequest(BaseModel):
    current_data: PortfolioData
    refinement: str

@router.post("/extract/resume")
async def extract_from_resume(file: UploadFile = File(...)):
    """
    Endpoint: POST /api/v1/portfolio/extract/resume
    
    Upload resume file and extract structured portfolio data
    """
    try:
        contents = await file.read()
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in ['pdf', 'docx', 'doc']:
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only PDF and DOCX are supported."
            )
        
        portfolio_data = await nlp_extractor.extract_from_resume(
            contents, 
            file_extension
        )
        
        return {
            "success": True,
            "data": portfolio_data.model_dump()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract/prompt")
async def extract_from_prompt(request: TextPromptRequest):
    """
    Endpoint: POST /api/v1/portfolio/extract/prompt
    
    Extract portfolio data from text description
    """
    try:
        portfolio_data = await nlp_extractor.extract_from_prompt(request.prompt)
        
        return {
            "success": True,
            "data": portfolio_data.model_dump()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_portfolio(request: PortfolioGenerateRequest):
    """
    Endpoint: POST /api/v1/portfolio/generate
    
    Generate HTML portfolio website from structured data
    """
    try:
        website_files = portfolio_generator.generate(
            request.data, 
            request.template
        )
        
        return {
            "success": True,
            "files": website_files
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine")
async def refine_portfolio(request: RefineRequest):
    """
    Endpoint: POST /api/v1/portfolio/refine
    
    Refine existing portfolio based on user feedback
    """
    try:
        refined_data = await nlp_extractor.refine_data(
            request.current_data,
            request.refinement
        )
        
        return {
            "success": True,
            "data": refined_data.model_dump()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_available_templates():
    """
    Endpoint: GET /api/v1/portfolio/templates
    
    Get list of available portfolio templates
    """
    return {
        "templates": [
            {
                "id": "template1",
                "name": "Modern Minimal",
                "description": "Clean and professional design with gradient header"
            },
            {
                "id": "template2",
                "name": "Creative",
                "description": "Bold and colorful design (coming soon)"
            },
            {
                "id": "template3",
                "name": "Corporate",
                "description": "Traditional business style (coming soon)"
            }
        ]
    }