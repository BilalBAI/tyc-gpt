"""
PDF Knowledge Base for AAOIFI Standards

This module extracts and provides searchable access to the AAOIFI Standards PDF.
Can be disabled via ENABLE_PDF_KNOWLEDGE environment variable (set to 'false' to disable).
"""

import os
from typing import List, Dict, Optional
import re

# Check if PDF knowledge base is enabled (default: True)
PDF_ENABLED = os.getenv('ENABLE_PDF_KNOWLEDGE', 'true').lower() != 'false'


class PDFKnowledgeBase:
    """
    A simple knowledge base for searching PDF content.
    For production, consider using vector embeddings (e.g., with OpenAI embeddings).
    """

    def __init__(self, pdf_path: str = "AAOIFI-Standards.pdf"):
        self.pdf_path = pdf_path
        self.content = None
        self.chunks = []

    def load_pdf(self) -> str:
        """
        Extract text from the PDF file.
        Returns the full text content.
        """
        try:
            import PyPDF2
        except ImportError:
            try:
                import pdfplumber
                return self._extract_with_pdfplumber()
            except ImportError:
                raise ImportError(
                    "Please install a PDF library: pip install PyPDF2 or pip install pdfplumber"
                )

        return self._extract_with_pypdf2()

    def _extract_with_pypdf2(self) -> str:
        """Extract text using PyPDF2."""
        import PyPDF2

        text_content = []
        max_pages = 100  # Limit pages to prevent memory issues
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                pages_to_process = min(total_pages, max_pages)
                
                for page_num in range(pages_to_process):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        if text and text.strip():
                            text_content.append(
                                f"--- Page {page_num + 1} ---\n{text}")
                    except Exception as e:
                        print(
                            f"Warning: Could not extract text from page {page_num + 1}: {e}")
                        continue
                
                if pages_to_process < total_pages:
                    print(f"Warning: Processed only first {pages_to_process} of {total_pages} pages to save memory")
        except Exception as e:
            raise Exception(f"Failed to load PDF: {e}")

        return "\n\n".join(text_content)

    def _extract_with_pdfplumber(self) -> str:
        """Extract text using pdfplumber (better for complex PDFs)."""
        import pdfplumber

        text_content = []
        max_pages = 100  # Limit pages to prevent memory issues
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_process = min(total_pages, max_pages)
                
                for page_num in range(pages_to_process):
                    try:
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        if text and text.strip():
                            text_content.append(
                                f"--- Page {page_num + 1} ---\n{text}")
                    except Exception as e:
                        print(
                            f"Warning: Could not extract text from page {page_num + 1}: {e}")
                        continue
                
                if pages_to_process < total_pages:
                    print(f"Warning: Processed only first {pages_to_process} of {total_pages} pages to save memory")
        except Exception as e:
            raise Exception(f"Failed to load PDF with pdfplumber: {e}")

        return "\n\n".join(text_content)

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks for better search.

        :param text: The text to chunk
        :param chunk_size: Size of each chunk in characters
        :param overlap: Overlap between chunks in characters
        :return: List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap  # Overlap for context

        return chunks

    def search(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Search for relevant content in the PDF.
        Returns a list of relevant text chunks.

        :param query: Search query
        :param max_results: Maximum number of results to return
        :return: List of dictionaries with 'text' and 'page' info
        """
        if self.content is None:
            try:
                print("Loading PDF content...")
                self.content = self.load_pdf()
                if not self.content:
                    print("Warning: PDF content is empty")
                    return []
                self.chunks = self.chunk_text(self.content)
            except Exception as e:
                print(f"Error loading PDF: {e}")
                self.content = ""  # Mark as attempted to prevent retries
                self.chunks = []
                return []

        query_lower = query.lower()
        query_terms = query_lower.split()

        # Score chunks based on term frequency
        scored_chunks = []
        for i, chunk in enumerate(self.chunks):
            chunk_lower = chunk.lower()
            score = sum(chunk_lower.count(term) for term in query_terms)
            if score > 0:
                # Extract page number if available
                page_match = re.search(r'--- Page (\d+) ---', chunk)
                page = page_match.group(1) if page_match else "Unknown"
                scored_chunks.append({
                    'text': chunk,
                    'score': score,
                    'page': page
                })

        # Sort by score and return top results
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        return scored_chunks[:max_results]

    def get_relevant_context(self, query: str, max_chars: int = 2000) -> str:
        """
        Get relevant context from the PDF for a given query.
        Returns formatted text that can be added to the prompt.

        :param query: The user's question or topic
        :param max_chars: Maximum characters to return
        :return: Formatted context string
        """
        results = self.search(query, max_results=5)

        if not results:
            return ""

        context_parts = []
        total_chars = 0

        for result in results:
            text = result['text']
            page = result['page']

            # Truncate if needed
            if total_chars + len(text) > max_chars:
                remaining = max_chars - total_chars
                text = text[:remaining] + "..."

            context_parts.append(f"[AAOIFI Standards - Page {page}]\n{text}")
            total_chars += len(text)

            if total_chars >= max_chars:
                break

        return "\n\n".join(context_parts)


# Global instance
_knowledge_base = None


def get_knowledge_base() -> PDFKnowledgeBase:
    """Get or create the global knowledge base instance."""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = PDFKnowledgeBase()
    return _knowledge_base


def get_aaoifi_context(query: str, max_chars: int = 2000) -> str:
    """
    Convenience function to get AAOIFI context for a query.
    Returns empty string if PDF cannot be loaded (graceful failure).

    :param query: The user's question
    :param max_chars: Maximum characters to return
    :return: Formatted context string (empty if PDF unavailable)
    """
    # Check if PDF is disabled via environment variable
    if not PDF_ENABLED:
        return ""
    
    try:
        kb = get_knowledge_base()
        return kb.get_relevant_context(query, max_chars)
    except Exception as e:
        print(f"Warning: Could not get AAOIFI context: {e}")
        return ""  # Return empty string to allow app to continue without PDF
