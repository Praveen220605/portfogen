import PyPDF2
import docx
from typing import Optional
import io

class ResumeParser:
    """
    Extracts text content from resume files (PDF and DOCX)
    """
    
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_bytes: PDF file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            # Create a file-like object from bytes
            pdf_file = io.BytesIO(file_bytes)
            
            # Create PDF reader
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_bytes: DOCX file content as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            # Create a file-like object from bytes
            docx_file = io.BytesIO(file_bytes)
            
            # Open document
            doc = docx.Document(docx_file)
            
            # Extract text from all paragraphs
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def parse_resume(file_bytes: bytes, file_type: str) -> str:
        """
        Main method - routes to appropriate parser based on file type
        
        Args:
            file_bytes: File content as bytes
            file_type: File extension (pdf, docx, doc)
            
        Returns:
            Extracted text as string
        """
        if file_type.lower() == "pdf":
            return ResumeParser.parse_pdf(file_bytes)
        elif file_type.lower() in ["docx", "doc"]:
            return ResumeParser.parse_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")