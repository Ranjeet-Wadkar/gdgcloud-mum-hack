"""
PDF and text parsing utilities for research papers.
"""

import PyPDF2
import io
from typing import Optional

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text content from uploaded PDF file.
    
    Args:
        pdf_file: Uploaded file object from Streamlit
    
    Returns:
        Extracted text content
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def clean_text(text: str) -> str:
    """
    Clean and preprocess extracted text.
    
    Args:
        text: Raw text content
    
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        cleaned_line = ' '.join(line.split())
        if cleaned_line and len(cleaned_line) > 10:  # Filter out very short lines
            cleaned_lines.append(cleaned_line)
    
    return '\n'.join(cleaned_lines)

def extract_key_sections(text: str) -> dict:
    """
    Extract key sections from research paper text.
    
    Args:
        text: Full text content
    
    Returns:
        Dictionary with extracted sections
    """
    sections = {
        'abstract': '',
        'introduction': '',
        'methodology': '',
        'results': '',
        'conclusion': '',
        'full_text': text
    }
    
    # Simple keyword-based section extraction
    text_lower = text.lower()
    
    # Find abstract
    abstract_keywords = ['abstract', 'summary']
    for keyword in abstract_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            # Extract next 500 characters as abstract
            sections['abstract'] = text[start_idx:start_idx + 500]
            break
    
    # Find introduction
    intro_keywords = ['introduction', 'background', 'overview']
    for keyword in intro_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            sections['introduction'] = text[start_idx:start_idx + 800]
            break
    
    # Find methodology
    method_keywords = ['methodology', 'methods', 'approach', 'experimental']
    for keyword in method_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            sections['methodology'] = text[start_idx:start_idx + 1000]
            break
    
    # Find results
    results_keywords = ['results', 'findings', 'outcomes']
    for keyword in results_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            sections['results'] = text[start_idx:start_idx + 1000]
            break
    
    # Find conclusion
    conclusion_keywords = ['conclusion', 'discussion', 'summary']
    for keyword in conclusion_keywords:
        if keyword in text_lower:
            start_idx = text_lower.find(keyword)
            sections['conclusion'] = text[start_idx:start_idx + 500]
            break
    
    return sections

def validate_text_input(text: str) -> bool:
    """
    Validate that the input text is sufficient for analysis.
    
    Args:
        text: Input text to validate
    
    Returns:
        True if text is valid, False otherwise
    """
    if not text or len(text.strip()) < 100:
        return False
    
    # Check for minimum word count
    word_count = len(text.split())
    if word_count < 50:
        return False
    
    return True
