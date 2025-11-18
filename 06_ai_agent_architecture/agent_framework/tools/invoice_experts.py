"""
Invoice Processing Expert Tools

Demonstrates both:
- Persona Pattern
- Document-as-Implementation Pattern
"""
import json
import os
from typing import Dict
from .registry import register_tool
from ..core.context import ActionContext


@register_tool(
    tags=["invoice_processing", "categorization", "expert"],
    description="Categorize an invoice expenditure using a financial expert."
)
def categorize_expenditure(action_context: ActionContext, description: str) -> str:
    """
    Categorize an invoice expenditure based on a short description.
    
    Uses PERSONA PATTERN: Acts as a senior financial analyst.
    
    Args:
        action_context: Context containing LLM
        description: A one-sentence summary of the expenditure
        
    Returns:
        A category name from the predefined set
    """
    from .llm_tools import prompt_expert
    
    categories = [
        "Office Supplies", "IT Equipment", "Software Licenses", "Consulting Services", 
        "Travel Expenses", "Marketing", "Training & Development", "Facilities Maintenance",
        "Utilities", "Legal Services", "Insurance", "Medical Services", "Payroll",
        "Research & Development", "Manufacturing Supplies", "Construction", "Logistics",
        "Customer Support", "Security Services", "Miscellaneous"
    ]
    
    return prompt_expert(
        action_context=action_context,
        description_of_expert="a senior financial analyst with deep expertise in corporate spending categorization and budget management",
        prompt=f"""Given the following expenditure description: '{description}'

Classify this expense into exactly ONE of these categories:
{', '.join(categories)}

Respond with ONLY the category name, nothing else."""
    )


@register_tool(
    tags=["invoice_processing", "validation", "expert"],
    description="Validate an invoice against company purchasing policies using a compliance expert."
)
def check_purchasing_rules(action_context: ActionContext, 
                           invoice_data: dict,
                           rules_file: str = "config/purchasing_rules.txt") -> dict:
    """
    Validate an invoice against company purchasing policies.
    
    Uses BOTH:
    - PERSONA PATTERN: Acts as a compliance officer
    - DOCUMENT-AS-IMPLEMENTATION: Loads rules from disk
    
    Args:
        action_context: Context containing LLM
        invoice_data: Extracted invoice details
        rules_file: Path to purchasing rules document
        
    Returns:
        Structured validation result
    """
    from .llm_tools import prompt_expert_for_json
    
    # DOCUMENT-AS-IMPLEMENTATION: Load rules from disk
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            purchasing_rules = f.read()
    except FileNotFoundError:
        purchasing_rules = "No purchasing rules file found. Assume all invoices require manual review."
    
    # Define validation schema
    validation_schema = {
        "type": "object",
        "required": ["compliant", "issues"],
        "properties": {
            "compliant": {"type": "boolean"},
            "issues": {"type": "string"},
            "required_actions": {
                "type": "array",
                "items": {"type": "string"}
            },
            "risk_level": {
                "type": "string",
                "enum": ["low", "medium", "high"]
            }
        }
    }
    
    # PERSONA PATTERN: Use compliance expert
    return prompt_expert_for_json(
        action_context=action_context,
        description_of_expert="a corporate procurement compliance officer with extensive knowledge of purchasing policies, vendor management, and financial controls",
        prompt=f"""Validate this invoice against our company purchasing policies.

Invoice Data:
{json.dumps(invoice_data, indent=2)}

Current Purchasing Policies:
{purchasing_rules}

Analyze whether this invoice complies with all policies. Respond with:
- compliant: true if it passes all checks, false if any violations found
- issues: Detailed explanation of any violations or concerns
- required_actions: List of actions needed (if any)
- risk_level: Assessment of compliance risk (low/medium/high)""",
        schema=validation_schema
    )


@register_tool(
    tags=["invoice_processing", "analysis", "expert"],
    description="Get expert analysis of invoice spending patterns."
)
def analyze_spending_pattern(action_context: ActionContext, 
                             invoices: list,
                             analysis_type: str = "general") -> str:
    """
    Analyze spending patterns across multiple invoices.
    
    Uses PERSONA PATTERN: Acts as a financial analyst.
    
    Args:
        action_context: Context containing LLM
        invoices: List of invoice data dictionaries
        analysis_type: Type of analysis (general, cost_optimization, risk_assessment)
        
    Returns:
        Expert analysis as a string
    """
    from .llm_tools import prompt_expert
    
    analysis_personas = {
        "general": "a senior financial analyst specializing in corporate spending analysis and budget optimization",
        "cost_optimization": "a cost reduction consultant with expertise in identifying savings opportunities",
        "risk_assessment": "a financial risk analyst with expertise in vendor relationships and payment patterns"
    }
    
    persona = analysis_personas.get(analysis_type, analysis_personas["general"])
    
    return prompt_expert(
        action_context=action_context,
        description_of_expert=persona,
        prompt=f"""Analyze these invoices and provide insights:

Invoices:
{json.dumps(invoices, indent=2)}

Provide a comprehensive analysis including:
1. Overall spending trends
2. Key findings or concerns
3. Recommendations for improvement"""
    )
