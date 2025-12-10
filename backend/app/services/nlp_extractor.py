from app.services.resume_parser import ResumeParser
from app.services.openai_service import OpenAIService
from app.models import PortfolioData

class NLPExtractor:
    """
    High-level service that coordinates resume parsing and NLP extraction
    """
    
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.openai_service = OpenAIService()
    
    async def extract_from_resume(self, file_bytes: bytes, file_type: str) -> PortfolioData:
        """
        Complete flow: File → Text → Structured Data
        
        Args:
            file_bytes: Resume file content as bytes
            file_type: File extension (pdf, docx, doc)
            
        Returns:
            Structured PortfolioData object
        """
        # Step 1: Extract text from file
        resume_text = self.resume_parser.parse_resume(file_bytes, file_type)
        
        # Step 2: Use AI to structure the data
        portfolio_data = self.openai_service.extract_portfolio_data(resume_text)
        
        return portfolio_data
    
    async def extract_from_prompt(self, prompt: str) -> PortfolioData:
        """
        Extract from user's text description
        
        Args:
            prompt: User's description
            
        Returns:
            Structured PortfolioData object
        """
        return self.openai_service.extract_from_prompt(prompt)
    
    async def refine_data(self, current_data: PortfolioData, refinement: str) -> PortfolioData:
        """
        Refine existing portfolio data
        
        Args:
            current_data: Current portfolio data
            refinement: Refinement request
            
        Returns:
            Updated PortfolioData object
        """
        return self.openai_service.refine_portfolio(current_data, refinement)