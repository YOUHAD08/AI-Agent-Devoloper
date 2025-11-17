"""
Support Ticket Processing Agent
Demonstrates: Unstructured text → Structured data → Action
"""
import os
import sys

current_file_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_file_dir)
sys.path.insert(0, parent_dir)

from agent_framework import (
    Goal,
    Agent,
    Environment,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    register_tool,
    generate_response,
    ActionContext
)

SAMPLE_SUPPORT_EMAIL = """
Subject: Can't login to my account - URGENT

Hi support,

I've been trying to log into my account for the past hour but I keep getting 
an "Invalid credentials" error. I'm 100% sure my password is correct because 
I have it saved in my password manager.

This is really frustrating because I have an important presentation in 2 hours 
and I need to access my files!

My username is: john.doe@company.com
Browser: Chrome on MacOS
Error: "Invalid credentials"

Please help ASAP!

Thanks,
John Doe
Account ID: ACC-12345
"""


@register_tool(tags=["support", "extraction"])
def extract_support_ticket(action_context: ActionContext, email_text: str) -> dict:
    """Extract support ticket information from customer email."""
    from agent_framework.tools.llm_tools import prompt_llm_for_json
    
    schema = {
        "type": "object",
        "required": ["issue_type", "urgency", "customer_info"],
        "properties": {
            "issue_type": {
                "type": "string",
                "enum": ["login_issue", "billing_issue", "bug_report", "feature_request", "other"]
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"]
            },
            "customer_info": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "account_id": {"type": "string"}
                }
            },
            "technical_details": {
                "type": "object",
                "properties": {
                    "browser": {"type": "string"},
                    "operating_system": {"type": "string"},
                    "error_message": {"type": "string"}
                }
            },
            "issue_summary": {"type": "string"},
            "customer_sentiment": {
                "type": "string",
                "enum": ["frustrated", "neutral", "satisfied", "angry"]
            }
        }
    }
    
    prompt = f"""
Extract support ticket information from this customer email.
Categorize the issue type, assess urgency, extract customer and technical details.
Also assess the customer's emotional state/sentiment.

Email:
{email_text}
"""
    
    return prompt_llm_for_json(action_context, schema, prompt)


@register_tool(tags=["support", "database"])
def create_support_ticket(ticket_data: dict) -> str:
    """Create a support ticket in the system."""
    print("\n" + "="*70)
    print("CREATING SUPPORT TICKET")
    print("="*70)
    print(f"Ticket ID: TICK-{hash(str(ticket_data)) % 100000:05d}")
    print(f"Issue Type: {ticket_data.get('issue_type')}")
    print(f"Urgency: {ticket_data.get('urgency')}")
    print(f"Customer: {ticket_data.get('customer_info', {}).get('name')}")
    print(f"Summary: {ticket_data.get('issue_summary')}")
    print("="*70 + "\n")
    
    ticket_id = f"TICK-{hash(str(ticket_data)) % 100000:05d}"
    return f"Support ticket {ticket_id} created successfully"


@register_tool(tags=["support", "routing"])
def assign_to_team(issue_type: str, urgency: str) -> str:
    """Assign ticket to appropriate support team."""
    
    # Routing logic
    teams = {
        "login_issue": "Authentication Team",
        "billing_issue": "Billing Team",
        "bug_report": "Engineering Team",
        "feature_request": "Product Team",
        "other": "General Support"
    }
    
    team = teams.get(issue_type, "General Support")
    
    # Urgent tickets get senior team members
    if urgency in ["high", "critical"]:
        team = f"Senior {team}"
    
    print(f"\n[ROUTING] Ticket assigned to: {team}\n")
    return f"Assigned to {team}"


@register_tool(tags=["support", "response"])
def generate_auto_response(action_context: ActionContext, ticket_data: dict) -> str:
    """Generate an automatic acknowledgment response to customer."""
    from agent_framework.tools.llm_tools import transform_text
    
    context = f"""
Customer: {ticket_data.get('customer_info', {}).get('name')}
Issue: {ticket_data.get('issue_summary')}
Urgency: {ticket_data.get('urgency')}
Sentiment: {ticket_data.get('customer_sentiment')}
"""
    
    instruction = """
Write a professional, empathetic acknowledgment email that:
1. Thanks the customer for reaching out
2. Acknowledges their issue specifically
3. Provides a ticket number (TICK-XXXXX)
4. Sets expectations for response time based on urgency
5. Includes a supportive, reassuring tone

Keep it concise (3-4 short paragraphs).
"""
    
    return transform_text(action_context, context, instruction)


@register_tool(tags=["support", "notification"])
def send_notification(recipient: str, ticket_id: str, urgency: str) -> str:
    """Send notification to support team."""
    print(f"\n[NOTIFICATION] Sent to {recipient}: New {urgency} priority ticket {ticket_id}\n")
    return f"Notification sent to {recipient}"


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution."""
    return message


def main():
    """Main function for support ticket processing workflow."""
    
    goals = [
        Goal(
            priority=1,
            name="Extract Ticket Data",
            description="Use extract_support_ticket to parse email and extract structured ticket information"
        ),
        Goal(
            priority=2,
            name="Create Ticket",
            description="Use create_support_ticket to create a ticket in the system with extracted data"
        ),
        Goal(
            priority=3,
            name="Route to Team",
            description="Use assign_to_team to route the ticket based on issue type and urgency"
        ),
        Goal(
            priority=4,
            name="Generate Response",
            description="Use generate_auto_response to create an acknowledgment email for the customer"
        ),
        Goal(
            priority=5,
            name="Notify Team",
            description="If urgent, use send_notification to alert the assigned team"
        ),
        Goal(
            priority=6,
            name="Complete",
            description="Call terminate with summary of ticket processing"
        )
    ]

    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["support", "system", "llm"]
        ),
        generate_response=generate_response,
        environment=Environment()
    )

    print("=" * 70)
    print("Support Ticket Processing Agent")
    print("=" * 70)
    print("\nProcessing support email...\n")
    
    task = f"""
Process this support email through the complete workflow:
1. Extract ticket information (issue type, urgency, customer details, sentiment)
2. Create a support ticket in the system
3. Route to the appropriate team
4. Generate an auto-response email
5. If high/critical urgency, send notification to team
6. Terminate with summary

Support Email:
{SAMPLE_SUPPORT_EMAIL}
"""
    
    agent.run(task, max_iterations=25)
    
    print()
    print("=" * 70)
    print("Support Ticket Processing Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()