from typing import Any, Optional
from .registry import register_tool
from ..core.context import ActionContext

@register_tool(
    tags=["storage", "invoices"],
    description="Store invoice data in persistent storage"
)
def store_invoice(action_context: ActionContext, invoice_data: dict) -> dict:
    """
    Store an invoice in persistent storage.
    
    Args:
        action_context: Context containing storage
        invoice_data: The invoice data to store
        
    Returns:
        Storage result with invoice number
    """
    storage = action_context.get_storage()
    
    if not storage:
        raise ValueError("Storage not available in action context")
    
    invoice_number = invoice_data.get("invoice_number")
    if not invoice_number:
        raise ValueError("Invoice data must contain an invoice_number")
    
    # Store in "invoices" collection
    storage.set_in_collection("invoices", invoice_number, invoice_data)
    
    return {
        "status": "success",
        "message": f"Stored invoice {invoice_number}",
        "invoice_number": invoice_number
    }


@register_tool(
    tags=["storage", "invoices"],
    description="Retrieve invoice data from storage"
)
def get_invoice(action_context: ActionContext, invoice_number: str) -> Optional[dict]:
    """
    Retrieve an invoice from storage.
    
    Args:
        action_context: Context containing storage
        invoice_number: The invoice number to retrieve
        
    Returns:
        Invoice data if found, None otherwise
    """
    storage = action_context.get_storage()
    
    if not storage:
        raise ValueError("Storage not available in action context")
    
    invoice = storage.get_from_collection("invoices", invoice_number)
    
    if invoice:
        return {
            "status": "found",
            "invoice": invoice
        }
    else:
        return {
            "status": "not_found",
            "message": f"Invoice {invoice_number} not found"
        }


@register_tool(
    tags=["storage", "invoices"],
    description="List all stored invoices"
)
def list_invoices(action_context: ActionContext) -> dict:
    """
    List all invoices in storage.
    
    Args:
        action_context: Context containing storage
        
    Returns:
        Dictionary of all invoices
    """
    storage = action_context.get_storage()
    
    if not storage:
        raise ValueError("Storage not available in action context")
    
    invoices = storage.list_collection("invoices")
    
    return {
        "status": "success",
        "count": len(invoices),
        "invoice_numbers": list(invoices.keys())
    }


@register_tool(
    tags=["storage", "generic"],
    description="Store any data in persistent storage"
)
def store_data(action_context: ActionContext, collection: str, key: str, data: Any) -> dict:
    """
    Store arbitrary data in persistent storage.
    
    Args:
        action_context: Context containing storage
        collection: Collection name (like a table)
        key: Unique identifier for the data
        data: The data to store
        
    Returns:
        Storage result
    """
    storage = action_context.get_storage()
    
    if not storage:
        raise ValueError("Storage not available in action context")
    
    storage.set_in_collection(collection, key, data)
    
    return {
        "status": "success",
        "message": f"Stored {key} in {collection}",
        "collection": collection,
        "key": key
    }


@register_tool(
    tags=["storage", "generic"],
    description="Retrieve data from persistent storage"
)
def get_data(action_context: ActionContext, collection: str, key: str) -> Optional[dict]:
    """
    Retrieve data from persistent storage.
    
    Args:
        action_context: Context containing storage
        collection: Collection name
        key: Unique identifier
        
    Returns:
        Stored data if found
    """
    storage = action_context.get_storage()
    
    if not storage:
        raise ValueError("Storage not available in action context")
    
    data = storage.get_from_collection(collection, key)
    
    if data is not None:
        return {
            "status": "found",
            "data": data
        }
    else:
        return {
            "status": "not_found",
            "message": f"Key '{key}' not found in collection '{collection}'"
        }