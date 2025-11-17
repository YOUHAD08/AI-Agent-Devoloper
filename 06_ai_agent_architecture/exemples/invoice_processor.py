"""
Invoice Processing Agent - Demonstrates self-prompting capabilities
"""
from datetime import datetime
import json
import os
import sys
from typing import Dict

# Add parent directory to path
current_file_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_file_dir)
#  sys.path is the list of folders Python searches for imports.
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

# Sample invoice text
SAMPLE_INVOICE = """
INVOICE

ABC Company Inc.
123 Business Street
New York, NY 10001
Tax ID: 12-3456789

Bill To:
XYZ Corporation
456 Client Avenue
Los Angeles, CA 90001

Invoice Number: INV-2024-001
Date: January 15, 2024
Due Date: February 15, 2024

Description                 Quantity    Unit Price    Total
---------------------------------------------------------------
Professional Services          40 hrs      $150.00   $6,000.00
Software License                5          $200.00   $1,000.00
Support Package                 1        $1,500.00   $1,500.00
---------------------------------------------------------------
                                          Subtotal:   $8,500.00
                                               Tax:     $850.00
                                             TOTAL:   $9,350.00

Payment Terms: Net 30
Please make checks payable to ABC Company Inc.
"""


@register_tool(tags=["document_processing", "invoices"])
def extract_invoice_data(action_context: ActionContext, document_text: str) -> dict:
    """
    Extract standardized invoice data from document text.
    This is a SPECIALIZED tool with a fixed schema.
    """
    from agent_framework.tools.llm_tools import prompt_llm_for_json
    
    # Define a fixed schema for invoice data
    invoice_schema = {
        "type": "object",
        "required": ["invoice_number", "date", "amount"],
        "properties": {
            "invoice_number": {"type": "string"},
            "date": {"type": "string"},
            "amount": {
                "type": "object",
                "properties": {
                    "subtotal": {"type": "number"},
                    "tax": {"type": "number"},
                    "total": {"type": "number"},
                    "currency": {"type": "string"}
                },
                "required": ["total", "currency"]
            },
            "vendor": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "tax_id": {"type": "string"},
                    "address": {"type": "string"}
                },
                "required": ["name"]
            },
            "client": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "address": {"type": "string"}
                }
            },
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "total": {"type": "number"}
                    },
                    "required": ["description", "total"]
                }
            }
        }
    }

    # Create a focused prompt
    extraction_prompt = f"""
Extract invoice information from the following document text. 
Focus on identifying:
- Invoice number (usually labeled as 'Invoice #', 'Invoice Number', etc.)
- Date (labeled as 'Date', 'Invoice Date', etc.)
- Amount details (subtotal, tax, total)
- Vendor information (company name, tax ID, address)
- Client information (bill to)
- Line items (individual charges and their details)

Document text:
{document_text}
"""
    
    # Use the general extraction tool with specialized schema
    return prompt_llm_for_json(
        action_context=action_context,
        schema=invoice_schema,
        prompt=extraction_prompt
    )


@register_tool(tags=["database", "invoices"])
def save_invoice_to_database(invoice_data: dict) -> str:
    """
    Save extracted invoice data as a JSON file.
    
    """

    # Create folder if it doesn't exist
    save_dir = os.path.join(current_file_dir, "invoices_db")
    os.makedirs(save_dir, exist_ok=True)

    # Create a safe filename
    invoice_number = invoice_data.get("invoice_number", "unknown")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"invoice_{invoice_number}_{timestamp}.json"
    file_path = os.path.join(save_dir, filename)

    # Save as JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(invoice_data, f, indent=4)

    return f"Invoice saved as JSON: {file_path}"


@register_tool(tags=["validation"])
def validate_invoice_data(invoice_data: dict) -> dict:
    """
    Validate that invoice data meets business rules.
    Returns validation result with any errors.
    """
    errors = []
    warnings = []
    
    # Check required fields
    if not invoice_data.get("invoice_number"):
        errors.append("Missing invoice number")
    
    if not invoice_data.get("amount", {}).get("total"):
        errors.append("Missing total amount")
    
    if not invoice_data.get("vendor", {}).get("name"):
        errors.append("Missing vendor name")
    
    # Check data consistency
    amount_info = invoice_data.get("amount", {})
    if amount_info.get("subtotal") and amount_info.get("tax") and amount_info.get("total"):
        expected_total = amount_info["subtotal"] + amount_info["tax"]
        actual_total = amount_info["total"]
        if abs(expected_total - actual_total) > 0.01:
            warnings.append(f"Total amount mismatch: expected ${expected_total}, got ${actual_total}")
    
    is_valid = len(errors) == 0
    
    return {
        "valid": is_valid,
        "errors": errors,
        "warnings": warnings
    }


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution."""
    return f"{message}"


def main():
    """Main function to run the invoice processor agent."""
    
    goals = [
        Goal(
            priority=1,
            name="Extract Invoice Data",
            description="Use extract_invoice_data tool to parse the invoice and extract structured information"
        ),
        Goal(
            priority=2,
            name="Validate Data",
            description="Use validate_invoice_data tool to ensure the extracted data is complete and consistent"
        ),
        Goal(
            priority=3,
            name="Save to Database",
            description="If validation passes, use save_invoice_to_database tool to store the invoice data"
        ),
        Goal(
            priority=4,
            name="Finish",
            description="Call terminate with a summary of what was accomplished"
        )
    ]

    # Create agent with document processing and system tools
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(tags=["document_processing", "invoices", "database", "validation", "system", "llm"]),
        generate_response=generate_response,
        environment=Environment()
    )

    print("=" * 70)
    print("Invoice Processing Agent")
    print("=" * 70)
    print("\nProcessing invoice...\n")
    
    task = f"""
Process this invoice by:
1. Extracting all relevant data using extract_invoice_data
2. Validating the extracted data
3. Saving to database if valid
4. Terminating with a summary

Invoice text:
{SAMPLE_INVOICE}
"""
    
    agent.run(task, max_iterations=20)
    
    print()
    print("=" * 70)
    print("Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()