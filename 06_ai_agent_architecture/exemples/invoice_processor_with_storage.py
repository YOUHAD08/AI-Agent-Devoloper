"""
Complete Invoice Processing System with Persistent Storage
Demonstrates: Extraction → Validation → Storage → Retrieval
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
from agent_framework.core.storage import Storage

# Multiple sample invoices
INVOICES = [
    """
INVOICE
XYZ Corp
Invoice #: INV-001
Date: 2024-01-15
Total: $5,000.00

Items:
- Consulting Services: $5,000.00
""",
    """
INVOICE
ABC Company  
Invoice Number: INV-002
Date: January 20, 2024
Total Amount: $3,500.00

Line Items:
- Software License: $2,000.00
- Support: $1,500.00
""",
    """
BILL FROM: Tech Solutions Inc.
Reference: INV-003
Issue Date: 01/25/2024
Amount Due: $7,200.00

Description:
- Hardware: $4,000.00
- Installation: $2,000.00
- Training: $1,200.00
"""
]


@register_tool(tags=["document_processing", "invoices"])
def extract_invoice_data(action_context: ActionContext, document_text: str) -> dict:
    """
    Extract standardized invoice data from document text.
    SPECIALIZED tool with focused prompting.
    """
    from agent_framework.tools.llm_tools import prompt_llm_for_json
    
    invoice_schema = {
        "type": "object",
        "required": ["invoice_number", "date", "total_amount"],
        "properties": {
            "invoice_number": {"type": "string"},
            "date": {"type": "string"},
            "total_amount": {"type": "number"},
            "vendor": {
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
                    }
                }
            }
        }
    }

    extraction_prompt = f"""
You are an expert invoice analyzer. Extract invoice information accurately.
Pay special attention to:
- Invoice numbers (look for 'Invoice #', 'No.', 'Reference', etc.)
- Dates (focus on invoice date or issue date)
- Amounts (ensure you capture the total amount correctly)
- Line items (capture all individual charges)

Stop and think step by step. Then extract the invoice data from:

<invoice>
{document_text}
</invoice>
"""
    
    return prompt_llm_for_json(
        action_context=action_context,
        schema=invoice_schema,
        prompt=extraction_prompt
    )


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution."""
    return message


def process_invoices():
    """Process multiple invoices and store them."""
    
    # Create shared storage (persists across runs)
    save_dir = os.path.join(current_file_dir, "invoices_db", "invoices.json")
    storage = Storage(storage_path=save_dir)
    
    goals = [
        Goal(
            priority=1,
            name="Persona",
            description="You are an Invoice Processing Agent, specialized in handling and storing invoice data."
        ),
        Goal(
            priority=2,
            name="Process All Invoices",
            description="""
Process each invoice by:
1. Extracting all important information using extract_invoice_data
2. Storing the extracted data using store_invoice
3. Confirming successful processing
4. Moving to the next invoice

After processing all invoices, use list_invoices to show what was stored.
Then terminate with a summary.
"""
        )
    ]

    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["document_processing", "invoices", "storage", "system", "llm"]
        ),
        generate_response=generate_response,
        environment=Environment(),
        storage=storage  
    )

    print("=" * 70)
    print("Invoice Processing System with Persistent Storage")
    print("=" * 70)
    print(f"\nProcessing {len(INVOICES)} invoices...\n")
    
    # Format all invoices for the agent
    invoice_text = "\n\n---NEXT INVOICE---\n\n".join(
        [f"Invoice {i+1}:\n{inv}" for i, inv in enumerate(INVOICES)]
    )
    
    task = f"""
Process these invoices:

{invoice_text}

For each invoice:
1. Extract the data
2. Store it
3. Confirm storage

Then list all stored invoices and terminate with summary.
"""
    
    agent.run(task, max_iterations=40)
    
    print()
    print("=" * 70)
    print("Processing Complete")
    print("=" * 70)
    
    # Show what was stored
    print("\n" + "=" * 70)
    print("STORED INVOICES")
    print("=" * 70)
    invoices = storage.list_collection("invoices")
    for inv_num, inv_data in invoices.items():
        print(f"\n{inv_num}:")
        print(f"  Date: {inv_data.get('date')}")
        print(f"  Total: ${inv_data.get('total_amount')}")
        print(f"  Vendor: {inv_data.get('vendor', {}).get('name', 'N/A')}")
    print("=" * 70)


def query_invoices():
    """Query previously stored invoices."""
    
    # Load existing storage
    storage = Storage(storage_path="invoices.json")
    
    goals = [
        Goal(
            priority=1,
            name="Query Invoices",
            description="""
You are an Invoice Query Agent.
Use list_invoices to see all stored invoices.
Then use get_invoice to retrieve specific invoice details.
Provide a summary of what you find.
"""
        )
    ]

    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["storage", "invoices", "system", "llm"]
        ),
        generate_response=generate_response,
        environment=Environment(),
        storage=storage
    )

    print("\n" + "=" * 70)
    print("Querying Stored Invoices")
    print("=" * 70)
    print()
    
    task = """
Query the invoice database:
1. List all stored invoices
2. Get details for each invoice
3. Provide a summary of total amounts
4. Terminate with findings
"""
    
    agent.run(task, max_iterations=20)
    
    print()
    print("=" * 70)
    print("Query Complete")
    print("=" * 70)


def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "query":
        query_invoices()
    else:
        process_invoices()
        print("\n\nTo query stored invoices, run: python invoice_processor_with_storage.py query")


if __name__ == "__main__":
    main()