"""
Horizontal Scaling Demo
Shows how the same framework creates different specialized agents
through tool selection.
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
    generate_response
)


def create_invoice_agent():
    """Specialized agent for invoice processing"""
    goals = [
        Goal(
            priority=1,
            name="Invoice Specialist",
            description="You are an invoice processing specialist. You extract and store invoice data."
        )
    ]
    
    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["document_processing", "invoices", "storage"]  # ← Only invoice tools
        ),
        generate_response=generate_response,
        environment=Environment()
    )


def create_support_agent():
    """Specialized agent for customer support"""
    goals = [
        Goal(
            priority=1,
            name="Support Specialist",
            description="You are a customer support specialist. You handle support tickets and emails."
        )
    ]
    
    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["support", "email", "storage"]  # ← Only support tools
        ),
        generate_response=generate_response,
        environment=Environment()
    )


def create_analysis_agent():
    """Specialized agent for data analysis"""
    goals = [
        Goal(
            priority=1,
            name="Analysis Specialist",
            description="You are a data analysis specialist. You analyze text and extract insights."
        )
    ]
    
    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["llm", "analysis", "extraction"]  # ← Only analysis tools
        ),
        generate_response=generate_response,
        environment=Environment()
    )


def create_super_agent():
    """General-purpose agent with all capabilities"""
    goals = [
        Goal(
            priority=1,
            name="General Assistant",
            description="You are a general-purpose assistant with access to many capabilities."
        )
    ]
    
    return Agent(
        goals=goals,
        agent_language=AgentFunctionCallingActionLanguage(),
        action_registry=PythonActionRegistry(
            tags=["document_processing", "support", "email", "llm", "storage", "analysis"]  # ← All tools!
        ),
        generate_response=generate_response,
        environment=Environment()
    )


def demo():
    print("=" * 70)
    print("HORIZONTAL SCALING DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstrates how the same framework creates different")
    print("specialized agents through tool selection (tags).")
    print()
    
    print("-" * 70)
    print("1. INVOICE AGENT")
    print("-" * 70)
    invoice_agent = create_invoice_agent()
    print(f"Available actions: {len(invoice_agent.actions.get_actions())}")
    print(f"Action names: {[a.name for a in invoice_agent.actions.get_actions()]}")
    print()
    
    print("-" * 70)
    print("2. SUPPORT AGENT")
    print("-" * 70)
    support_agent = create_support_agent()
    print(f"Available actions: {len(support_agent.actions.get_actions())}")
    print(f"Action names: {[a.name for a in support_agent.actions.get_actions()]}")
    print()
    
    print("-" * 70)
    print("3. ANALYSIS AGENT")
    print("-" * 70)
    analysis_agent = create_analysis_agent()
    print(f"Available actions: {len(analysis_agent.actions.get_actions())}")
    print(f"Action names: {[a.name for a in analysis_agent.actions.get_actions()]}")
    print()
    
    print("-" * 70)
    print("4. SUPER AGENT (All Tools)")
    print("-" * 70)
    super_agent = create_super_agent()
    print(f"Available actions: {len(super_agent.actions.get_actions())}")
    print(f"Action names: {[a.name for a in super_agent.actions.get_actions()]}")
    print()
    
    print("=" * 70)
    print("KEY INSIGHT:")
    print("=" * 70)
    print("✓ Same Agent class")
    print("✓ Same framework")
    print("✓ Different capabilities through tool selection")
    print("✓ Easy to add new tools without changing agent code")
    print("✓ Modular, scalable, maintainable")
    print("=" * 70)


if __name__ == "__main__":
    demo()