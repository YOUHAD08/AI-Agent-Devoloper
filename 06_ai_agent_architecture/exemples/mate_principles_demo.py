"""
MATE Design Principles Demonstration

Shows all four principles:
- Model Efficiency
- Action Specificity
- Token Efficiency
- Environmental Safety
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
    ActionContext,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    generate_response
)


def demo_model_efficiency():
    """Demonstrate choosing the right model for the task."""
    print("\n" + "=" * 80)
    print("PRINCIPLE 1: MODEL EFFICIENCY")
    print("=" * 80)
    
    print("""
CONCEPT: Use the right model for the right task
- Simple tasks (extraction, classification) → Fast model (cheap, quick)
- Complex tasks (analysis, reasoning) → Powerful model (accurate, thorough)

BENEFIT: Save costs and time without sacrificing quality
    """)
    
    print("Example comparison:")
    print("""
Task: Extract email from text
  Traditional: Use powerful model (gpt-4) for simple extraction
  MATE: Use fast model (gpt-3.5-turbo) for simple extraction
  Savings: 10x cheaper, 5x faster, same accuracy

Task: Analyze contradictions in technical documentation  
  Traditional: Use fast model (might miss subtleties)
  MATE: Use powerful model (gpt-4) for thorough analysis
  Benefit: Better accuracy, catches real issues
    """)


def demo_action_specificity():
    """Demonstrate specific vs. generic actions."""
    print("\n" + "=" * 80)
    print("PRINCIPLE 2: ACTION SPECIFICITY")
    print("=" * 80)
    
    print("""
CONCEPT: Design actions with specific, limited scope
- Generic action: Can do anything (but risky)
- Specific action: Can do ONE thing, safely

BENEFIT: Harder to misuse, built-in safety checks
    """)
    
    print("\nComparison:")
    print("""
GENERIC (Risky):
  @register_tool()
  def modify_calendar(event_id, updates):
      return calendar.update(event_id, updates)
  
  Problems:
  - Can delete events
  - Can change organizers
  - No validation
  
SPECIFIC (Safe):
  @register_tool()
  def reschedule_my_meeting(event_id, new_time, duration):
      # Check: I own this meeting
      # Check: New time is in future
      # Check: Duration is 15-120 minutes
      # Only reschedule, nothing else
      return calendar.update_time(event_id, new_time, duration)
  
  Benefits:
  - Only reschedules
  - Only if I own it
  - Built-in validation
  - Hard to misuse
    """)


def demo_token_efficiency():
    """Demonstrate efficient vs. wasteful prompts."""
    print("\n" + "=" * 80)
    print("PRINCIPLE 3: TOKEN EFFICIENCY")
    print("=" * 80)
    
    print("""
CONCEPT: Request only what you need, use focused prompts
- Verbose prompt: Wastes input tokens
- Specific prompt: Gets exactly what you need

BENEFIT: Lower costs, faster responses
    """)
    
    # Calculate token waste
    verbose_prompt = """
    Please analyze this sales data thoroughly. I would like you to consider 
    many different aspects including monthly trends, seasonal patterns, 
    year-over-year growth, product category performance, regional variations, 
    customer segments, and comprehensive insights about all these aspects.
    Give me a detailed and comprehensive analysis.
    """
    
    efficient_prompt = """
    Sales Data: [data]
    1. Calculate YoY growth
    2. Identify top 3 trends
    3. Flag anomalies
    """
    
    verbose_tokens = len(verbose_prompt) // 4
    efficient_tokens = len(efficient_prompt) // 4
    savings = ((verbose_tokens - efficient_tokens) / verbose_tokens) * 100
    
    print(f"\nExample comparison:")
    print(f"  Verbose prompt: {verbose_tokens} tokens")
    print(f"  Efficient prompt: {efficient_tokens} tokens")
    print(f"  Savings: {savings:.0f}%")
    print(f"\n  Better: Short, specific prompt gets same result with fewer tokens")


def demo_environmental_safety():
    """Demonstrate reversible actions and transactions."""
    print("\n" + "=" * 80)
    print("PRINCIPLE 4: ENVIRONMENTAL SAFETY")
    print("=" * 80)
    
    print("""
CONCEPT: Protect against mistakes with reversible actions and transactions

Four patterns:

1. REVERSIBLE ACTIONS
   - Every action can be undone
   - Store enough info to reverse it
   - Example: Create event ↔ Delete event

2. TRANSACTIONS
   - Multiple actions treated as ONE unit
   - All succeed or ALL fail (no inconsistent states)
   - If step 3 fails, undo steps 1-2 automatically

3. STAGED EXECUTION
   - Stage actions for review before executing
   - Human or AI can approve/reject
   - Catch problems before permanent changes

4. COMPREHENSIVE TOOLS
   - One tool with all safety built-in
   - Better than many small risky tools
   - Example: schedule_meeting() vs. create_event() + send_email()

BENEFIT: Mistakes can be undone, system stays consistent
    """)
    
    print("\nExample: Schedule meeting with safety")
    print("""
    Transaction:
      1. Create calendar event ← Can be undone
      2. Send invite to Alice ← Can be undone
      3. Send invite to Bob   ← Can be undone
    
    If step 3 fails:
      - Step 2 automatically undone (invite to Bob not sent)
      - Step 1 automatically undone (event deleted)
      - System is consistent, no orphaned data
    
    Without safety: Event created but invites not sent = BAD STATE
    """)


def main():
    """Run all MATE principle demonstrations."""
    print("=" * 80)
    print("MATE DESIGN PRINCIPLES FOR AI AGENTS")
    print("=" * 80)
    print("""
MATE stands for:
M - Model Efficiency: Choose the right LLM for each task
A - Action Specificity: Design precise, limited-scope actions
T - Token Efficiency: Use tokens wisely, request only what you need
E - Environmental Safety: Protect against mistakes through reversibility
    """)
    
    # Run demos
    demo_model_efficiency()
    demo_action_specificity()
    demo_token_efficiency()
    demo_environmental_safety()
    
    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print("""
1. MODEL EFFICIENCY
   ✓ Fast model for simple extraction/classification
   ✓ Powerful model for complex reasoning/analysis
   ✓ Cost: 10x savings on simple tasks

2. ACTION SPECIFICITY
   ✓ Design ONE action to do ONE thing well
   ✓ Include all necessary validation
   ✓ Make it hard to misuse
   ✓ Safety: Fewer dangerous mistakes

3. TOKEN EFFICIENCY
   ✓ Short, focused prompts
   ✓ Request exactly what you need
   ✓ Structured output (JSON)
   ✓ Cost: 50%+ token savings

4. ENVIRONMENTAL SAFETY
   ✓ All actions reversible
   ✓ Transactions for consistency
   ✓ Staged execution for review
   ✓ Comprehensive tools vs. risky small tools
   ✓ Safety: Undo button for everything
    """)
    
    print("=" * 80)


if __name__ == "__main__":
    main()