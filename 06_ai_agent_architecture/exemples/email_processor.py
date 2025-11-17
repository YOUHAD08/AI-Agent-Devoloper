"""
Email Processing Agent - Complete workflow example
Demonstrates: Receive → Extract → Process → Decide
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

# Sample email
SAMPLE_EMAIL = """
From: john.client@company.com
To: sales@ourcompany.com
Subject: Meeting Request - Q1 Planning
Date: January 20, 2024

Hi Sales Team,

I'd like to schedule a meeting to discuss our Q1 planning and review the new product roadmap.

Would next Tuesday, January 30th at 2:00 PM PST work for everyone? We can meet at our office 
or do a video call if that's more convenient.

Please confirm your availability, and let me know if you have any agenda items to add.

Looking forward to connecting!

Best regards,
John Client
Senior Product Manager
john.client@company.com
(555) 123-4567
"""


@register_tool(tags=["email", "extraction"])
def extract_meeting_request(action_context: ActionContext, email_text: str) -> dict:
    """
    Extract meeting request details from email.
    SPECIALIZED tool with fixed schema.
    """
    from agent_framework.tools.llm_tools import prompt_llm_for_json
    
    schema = {
        "type": "object",
        "required": ["is_meeting_request", "proposed_date", "proposed_time"],
        "properties": {
            "is_meeting_request": {"type": "boolean"},
            "subject": {"type": "string"},
            "sender": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "title": {"type": "string"}
                }
            },
            "proposed_date": {"type": "string"},
            "proposed_time": {"type": "string"},
            "timezone": {"type": "string"},
            "location_preference": {"type": "string"},
            "agenda_items": {
                "type": "array",
                "items": {"type": "string"}
            },
            "attendees_requested": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
    
    prompt = f"""
Extract meeting request information from this email.
Focus on:
- Is this a meeting request? (true/false)
- Proposed date and time
- Sender information
- Location preference (office, video call, etc.)
- Agenda items mentioned
- Who should attend

Email:
{email_text}
"""
    
    return prompt_llm_for_json(action_context, schema, prompt)


@register_tool(tags=["calendar", "availability"])
def check_calendar_availability(date: str, time: str) -> dict:
    """
    Check if the proposed meeting time is available.
    (Mock implementation)
    """
    # Simulate checking calendar
    print(f"\n[CALENDAR] Checking availability for {date} at {time}...")
    
    # Mock logic: Tuesday afternoons are busy
    is_available = "Tuesday" not in date or "PM" not in time
    
    return {
        "available": is_available,
        "date": date,
        "time": time,
        "conflicts": [] if is_available else ["Team standup meeting"]
    }


@register_tool(tags=["email", "response"])
def send_email_response(to: str, subject: str, body: str) -> str:
    """
    Send an email response.
    (Mock implementation)
    """
    print("\n" + "="*70)
    print("SENDING EMAIL")
    print("="*70)
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"\n{body}")
    print("="*70 + "\n")
    
    return f"Email sent to {to}"


@register_tool(tags=["calendar", "scheduling"])
def create_calendar_event(meeting_data: dict) -> str:
    """
    Create a calendar event.
    (Mock implementation)
    """
    print("\n" + "="*70)
    print("CREATING CALENDAR EVENT")
    print("="*70)
    print(f"Subject: {meeting_data.get('subject')}")
    print(f"Date: {meeting_data.get('date')}")
    print(f"Time: {meeting_data.get('time')}")
    print(f"Attendees: {', '.join(meeting_data.get('attendees', []))}")
    print("="*70 + "\n")
    
    return "Calendar event created successfully"


@register_tool(tags=["email", "composition"])
def compose_meeting_response(action_context: ActionContext, 
                            meeting_data: dict, 
                            availability: dict,
                            tone: str = "professional") -> str:
    """
    Use LLM to compose an appropriate meeting response email.
    """
    from agent_framework.tools.llm_tools import transform_text
    
    context = f"""
Meeting Request Details:
- Subject: {meeting_data.get('subject')}
- Proposed: {meeting_data.get('proposed_date')} at {meeting_data.get('proposed_time')}
- From: {meeting_data.get('sender', {}).get('name')}

Availability Check Result:
- Available: {availability.get('available')}
- Conflicts: {', '.join(availability.get('conflicts', [])) if availability.get('conflicts') else 'None'}
"""
    
    if availability.get('available'):
        instruction = f"""
Write a {tone} email confirming the meeting.
Express enthusiasm about the meeting and confirm all details.
Keep it concise and friendly.
"""
    else:
        instruction = f"""
Write a {tone} email politely declining the proposed time due to conflicts.
Suggest alternative times (suggest 2-3 options within the same week).
Express continued interest in the meeting.
Keep it concise and apologetic.
"""
    
    return transform_text(action_context, context, instruction)


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution."""
    return message


def main():
    """Main function demonstrating complete email processing workflow."""
    
    goals = [
        Goal(
            priority=1,
            name="Extract Meeting Details",
            description="Use extract_meeting_request to parse the email and extract structured meeting information"
        ),
        Goal(
            priority=2,
            name="Check Availability",
            description="Use check_calendar_availability to see if the proposed time works"
        ),
        Goal(
            priority=3,
            name="Compose Response",
            description="Use compose_meeting_response to generate an appropriate email reply based on availability"
        ),
        Goal(
            priority=4,
            name="Send Response",
            description="Use send_email_response to send the composed email"
        ),
        Goal(
            priority=5,
            name="Create Event (if accepted)",
            description="If we accepted the meeting, use create_calendar_event to add it to the calendar"
        ),
        Goal(
            priority=6,
            name="Finish",
            description="Call terminate with a summary of actions taken"
        )
    ]

    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["email", "calendar", "system", "llm"]
        ),
        generate_response=generate_response,
        environment=Environment()
    )

    print("=" * 70)
    print("Email Processing Agent - Workflow Example")
    print("=" * 70)
    print("\nProcessing incoming email...\n")
    
    task = f"""
Process this email using the complete workflow:
1. Extract meeting request details
2. Check calendar availability
3. Compose appropriate response based on availability
4. Send the response
5. Create calendar event if accepting
6. Terminate with summary

Email:
{SAMPLE_EMAIL}
"""
    
    agent.run(task, max_iterations=30)
    
    print()
    print("=" * 70)
    print("Workflow Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()