"""
Document-as-Implementation Pattern Tools

These tools enable agents to load and use human-readable documents
as the source of truth for business logic.
"""
import os
from typing import Optional, List
from .registry import register_tool
from ..core.context import ActionContext


@register_tool(
    tags=["document", "file"],
    description="Load a document from disk for the agent to use."
)
def load_document(file_path: str) -> dict:
    """
    Load a document from disk.
    
    Implements DOCUMENT-AS-IMPLEMENTATION pattern.
    
    Args:
        file_path: Path to the document to load
        
    Returns:
        Dictionary with document content and metadata
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "status": "success",
            "file_path": file_path,
            "content": content,
            "size_bytes": len(content),
            "exists": True
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "file_path": file_path,
            "content": None,
            "error": "File not found",
            "exists": False
        }
    except Exception as e:
        return {
            "status": "error",
            "file_path": file_path,
            "content": None,
            "error": str(e),
            "exists": False
        }


@register_tool(
    tags=["document", "file", "list"],
    description="List all documents in a directory."
)
def list_documents(directory_path: str, extension: Optional[str] = None) -> dict:
    """
    List all documents in a directory.
    
    Args:
        directory_path: Path to the directory
        extension: Optional file extension filter (e.g., ".txt", ".md")
        
    Returns:
        Dictionary with list of files
    """
    try:
        if not os.path.exists(directory_path):
            return {
                "status": "error",
                "error": f"Directory not found: {directory_path}",
                "files": []
            }
        
        files = os.listdir(directory_path)
        
        if extension:
            files = [f for f in files if f.endswith(extension)]
        
        return {
            "status": "success",
            "directory": directory_path,
            "count": len(files),
            "files": sorted(files)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "files": []
        }


@register_tool(
    tags=["document", "file", "write"],
    description="Write content to a document file."
)
def write_document(file_path: str, content: str) -> dict:
    """
    Write content to a document file.
    
    Args:
        file_path: Path where document should be written
        content: Content to write
        
    Returns:
        Dictionary with write result
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "file_path": file_path,
            "bytes_written": len(content)
        }
    except Exception as e:
        return {
            "status": "error",
            "file_path": file_path,
            "error": str(e)
        }


@register_tool(
    tags=["document", "knowledge"],
    description="Load and combine multiple documents for comprehensive context."
)
def load_knowledge_base(file_paths: List[str]) -> dict:
    """
    Load multiple documents to create a comprehensive knowledge base.
    
    Useful for multi-document reasoning.
    
    Args:
        file_paths: List of document paths to load
        
    Returns:
        Dictionary with combined content and individual documents
    """
    documents = {}
    errors = []
    
    for path in file_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                documents[path] = f.read()
        except Exception as e:
            errors.append(f"{path}: {str(e)}")
    
    # Combine all documents
    combined = "\n\n---\n\n".join([
        f"Document: {path}\n\n{content}" 
        for path, content in documents.items()
    ])
    
    return {
        "status": "success" if documents else "error",
        "documents_loaded": len(documents),
        "documents": documents,
        "combined_content": combined,
        "errors": errors
    }