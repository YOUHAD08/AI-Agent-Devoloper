"""
Specific Action Tools

Demonstrates ACTION SPECIFICITY principle:
Design tools with clear, limited scope and built-in safety.
"""
from ..registry import register_tool
from ...core.context import ActionContext
from datetime import datetime, timedelta


@register_tool(
    tags=["calendar", "safe"],
    description="Reschedule a meeting you own to a specific new time"
)
def reschedule_my_meeting(action_context: ActionContext,
                         event_id: str,
                         new_start_time: str,
                         new_duration_minutes: int) -> dict:
    """
    Reschedule a meeting YOU OWN to a new time.
    
    Demonstrates ACTION SPECIFICITY:
    - Can ONLY reschedule
    - ONLY your own meetings
    - ONLY to valid future times
    - ONLY reasonable durations
    
    Args:
        action_context: Context with user info
        event_id: ID of meeting to reschedule
        new_start_time: ISO format datetime string
        new_duration_minutes: Duration in minutes
        
    Returns:
        Confirmation of reschedule
    """
    # Get user ID
    user_id = action_context.get("metadata", {}).get("user_id")
    if not user_id:
        raise ValueError("User ID not available in context")
    
    # Get event (mock implementation)
    event = {
        "id": event_id,
        "organizer": user_id,  # Mock
        "title": "Team Meeting"
    }
    
    # SAFETY CHECK 1: Verify ownership
    if event.get("organizer") != user_id:
        raise ValueError(f"Cannot reschedule: You do not own this meeting")
    
    # SAFETY CHECK 2: Parse and validate time
    try:
        new_start = datetime.fromisoformat(new_start_time)
    except ValueError:
        raise ValueError("Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS")
    
    # SAFETY CHECK 3: Ensure future time
    if new_start < datetime.now():
        raise ValueError("Cannot schedule meetings in the past")
    
    # SAFETY CHECK 4: Ensure not too far in future
    max_future = datetime.now() + timedelta(days=365)
    if new_start > max_future:
        raise ValueError("Cannot schedule more than 1 year in advance")
    
    # SAFETY CHECK 5: Validate duration
    if not 15 <= new_duration_minutes <= 120:
        raise ValueError("Duration must be between 15 and 120 minutes")
    
    # All checks passed - perform action
    return {
        "status": "success",
        "event_id": event_id,
        "new_start_time": new_start_time,
        "new_duration_minutes": new_duration_minutes,
        "confirmation": f"Meeting '{event['title']}' rescheduled"
    }


@register_tool(
    tags=["email", "safe"],
    description="Send an email to a verified recipient"
)
def send_email_to_verified(action_context: ActionContext,
                          recipient_email: str,
                          subject: str,
                          body: str,
                          max_recipients: int = 1) -> dict:
    """
    Send an email with safety constraints.
    
    Demonstrates ACTION SPECIFICITY:
    - ONLY to pre-verified recipients
    - ONLY single recipient (no mass emails)
    - Body length limit
    - No external attachments
    
    Args:
        action_context: Context with verified email list
        recipient_email: Email address to send to
        subject: Email subject
        body: Email body text
        max_recipients: Maximum allowed recipients
        
    Returns:
        Confirmation of send
    """
    # SAFETY CHECK 1: Verify recipient is approved
    verified_recipients = action_context.get("metadata", {}).get("verified_emails", [])
    
    if recipient_email not in verified_recipients:
        raise ValueError(f"Email {recipient_email} is not in verified recipient list")
    
    # SAFETY CHECK 2: Limit number of recipients
    if max_recipients > 1:
        raise ValueError("Can only send to 1 recipient at a time (prevents mass emails)")
    
    # SAFETY CHECK 3: Validate subject length
    if len(subject) > 200:
        raise ValueError("Subject line too long (max 200 characters)")
    
    # SAFETY CHECK 4: Validate body length
    if len(body) > 5000:
        raise ValueError("Email body too long (max 5000 characters)")
    
    # SAFETY CHECK 5: Check for suspicious content
    suspicious_patterns = ["password", "credit card", "ssn", "social security"]
    body_lower = body.lower()
    for pattern in suspicious_patterns:
        if pattern in body_lower:
            raise ValueError(f"Email cannot contain: {pattern}")
    
    # All checks passed
    return {
        "status": "success",
        "recipient": recipient_email,
        "subject": subject,
        "confirmation": "Email sent successfully"
    }


@register_tool(
    tags=["data", "safe"],
    description="Query database with specific, predefined queries"
)
def query_database_safe(action_context: ActionContext,
                       query_type: str,
                       parameters: dict) -> dict:
    """
    Query database using only pre-approved query types.
    
    Demonstrates ACTION SPECIFICITY:
    - ONLY predefined query types
    - ONLY specific parameters
    - Prevents SQL injection
    - Limits data access
    
    Args:
        action_context: Context with database access
        query_type: Type of query (get_user, get_sales, etc.)
        parameters: Query parameters (validated against type)
        
    Returns:
        Query results
    """
    # Define approved queries with their parameters
    approved_queries = {
        "get_user": {
            "params": ["user_id"],
            "fields": ["id", "name", "email"],
            "description": "Get user information by ID"
        },
        "get_sales_by_date": {
            "params": ["start_date", "end_date"],
            "fields": ["date", "amount", "product"],
            "description": "Get sales in date range"
        },
        "get_top_customers": {
            "params": ["limit"],
            "fields": ["customer_name", "total_spent"],
            "description": "Get top N customers by spending"
        }
    }
    
    # SAFETY CHECK 1: Query type must be approved
    if query_type not in approved_queries:
        raise ValueError(f"Query type '{query_type}' not approved")
    
    query_def = approved_queries[query_type]
    
    # SAFETY CHECK 2: Parameters must match approved list
    for param in parameters.keys():
        if param not in query_def["params"]:
            raise ValueError(f"Parameter '{param}' not allowed for query type '{query_type}'")
    
    # SAFETY CHECK 3: All required parameters present
    for required_param in query_def["params"]:
        if required_param not in parameters:
            raise ValueError(f"Missing required parameter: {required_param}")
    
    # Execute query (mock)
    return {
        "status": "success",
        "query_type": query_type,
        "parameters": parameters,
        "fields": query_def["fields"],
        "results": []  # Would be actual results
    }