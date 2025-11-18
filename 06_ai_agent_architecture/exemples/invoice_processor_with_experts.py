"""
Complete Invoice Processing with Expert Consultation

Demonstrates:
- Persona Pattern (financial analysts, compliance officers)
- Document-as-Implementation (loading purchasing rules)
- Self-prompting (extraction, categorization, validation)
- Persistent storage (saving results)
"""
import os
import sys
import json

current_file_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_file_dir)
sys.path.insert(0, parent_dir)

from agent_framework import (
    Goal,
    Agent,
    Environment,
    Storage,
    AgentFunctionCallingActionLanguage,
    PythonActionRegistry,
    register_tool,
    generate_response,
    ActionContext
)

# Sample invoices to process
SAMPLE_INVOICES = [
    """
    INVOICE #INV-2024-001
    Date: January 15, 2024
    From: Tech Solutions Inc.
    
    Items:
    - Laptop (Dell XPS 15): $2,000
    - External Monitor: $400
    - Software License (MS Office): $150
    
    Total: $2,550
    """,
    
    """
    INVOICE #INV-2024-002
    Date: January 20, 2024
    From: Management Consulting Group
    
    Services Rendered:
    - Strategic Planning Consultation: $12,000
    
    Total: $12,000
    
    Note: This is for Q1 strategic planning project
    """,
    
    """
    INVOICE #INV-2024-003
    Date: January 25, 2024
    From: Office Depot
    
    Items:
    - Printer Paper (50 reams): $250
    - Pens (bulk order): $75
    - Desk Organizers: $180
    
    Total: $505
    """
]


@register_tool(tags=["system"], terminal=True)
def terminate(message: str) -> str:
    """Terminates the agent's execution."""
    return message


def main():
    """
    Run the complete invoice processing workflow with expert consultation.
    """
    
    # Ensure config directory and rules file exist
    config_dir = os.path.join(parent_dir, "config")
    rules_file = os.path.join(config_dir, "purchasing_rules.txt")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Created config directory: {config_dir}")
    
    if not os.path.exists(rules_file):
        print(f"\nWARNING: Purchasing rules file not found at {rules_file}")
        print("Creating a sample rules file...")
        
        sample_rules = """COMPANY PURCHASING POLICY

APPROVAL REQUIREMENTS:
1. All purchases over $5,000 require pre-approval from department manager
2. Purchases over $10,000 require CFO approval

VENDOR REQUIREMENTS:
3. IT equipment must be purchased from approved vendors
4. All vendors must have current W-9 on file

DOCUMENTATION REQUIREMENTS:
5. Consulting fees over $10,000 require a Statement of Work (SOW)
6. All equipment purchases require asset tagging
"""
        with open(rules_file, 'w') as f:
            f.write(sample_rules)
        print(f"Created sample rules file at {rules_file}\n")
    
    # Create storage
    storage_dir = os.path.join(current_file_dir, "invoices_db")
    storage = Storage(storage_path=os.path.join(storage_dir, "invoice_processing_results.json"))
    
    # Define agent goals
    goals = [
        Goal(
            priority=1,
            name="Invoice Processing Specialist",
            description="""You are an Invoice Processing Agent specialized in handling and analyzing invoices efficiently and accurately.

Your expertise includes:
- Extracting structured data from invoices
- Categorizing expenditures appropriately
- Validating invoices against company policies
- Storing processed invoices with complete metadata"""
        ),
        Goal(
            priority=2,
            name="Process Invoices Comprehensively",
            description=f"""Process each invoice through the complete workflow:

1. EXTRACT: Use extract_invoice_data to parse the invoice and extract structured information

2. SUMMARIZE: Create a one-sentence description of what was purchased

3. CATEGORIZE: Use categorize_expenditure with your one-sentence description to classify the spending

4. VALIDATE: Use check_purchasing_rules to verify compliance with company policies
   - The rules are loaded from: {rules_file}
   - Pay attention to approval requirements and documentation needs

5. STORE: Use store_invoice to save the complete processed invoice including:
   - Original extracted data
   - Category assignment
   - Compliance validation result

6. REPORT: After processing all invoices, provide a summary of:
   - Total invoices processed
   - Categories breakdown
   - Compliance issues found
   - Recommended actions

7. TERMINATE: Call terminate with your summary"""
        )
    ]
    
    # Create agent with all necessary tools
    agent = Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=[
                "invoice_processing",      # Invoice expert tools
                "document",                 # Document loading tools
                "extraction",               # LLM extraction tools
                "expert",                   # Persona pattern tools
                "storage",                  # Storage tools
                "llm",                      # General LLM tools
                "system"                    # System tools (terminate)
            ]
        ),
        generate_response=generate_response,
        environment=Environment(),
        storage=storage
    )
    
    print("=" * 80)
    print("INVOICE PROCESSING SYSTEM WITH EXPERT CONSULTATION")
    print("=" * 80)
    print(f"\nProcessing {len(SAMPLE_INVOICES)} invoices...")
    print(f"Using purchasing rules from: {rules_file}\n")
    
    # Format invoices for the agent
    invoice_texts = "\n\n" + "="*80 + "\n\n".join([
        f"INVOICE {i+1}:\n{invoice}"
        for i, invoice in enumerate(SAMPLE_INVOICES)
    ])
    
    task = f"""Process these invoices using the complete workflow:

{invoice_texts}

For EACH invoice:
1. Extract the data
2. Create a brief one-sentence description
3. Categorize using the financial expert
4. Validate against purchasing policies
5. Store the complete result

Then provide a comprehensive summary and terminate.
"""
    
    agent.run(task, max_iterations=50)
    
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    
    # Display results
    print("\n" + "=" * 80)
    print("STORED INVOICE RESULTS")
    print("=" * 80)
    
    invoices = storage.list_collection("invoices")
    if invoices:
        for inv_num, inv_data in invoices.items():
            print(f"\n{inv_num}:")
            print(f"  Amount: ${inv_data.get('total_amount', 'N/A')}")
            print(f"  Category: {inv_data.get('category', 'N/A')}")
            
            validation = inv_data.get('validation', {})
            if validation:
                compliant = validation.get('compliant', False)
                status = "✓ COMPLIANT" if compliant else "✗ NON-COMPLIANT"
                print(f"  Compliance: {status}")
                if not compliant:
                    print(f"  Issues: {validation.get('issues', 'N/A')}")
    else:
        print("\nNo invoices were stored.")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()