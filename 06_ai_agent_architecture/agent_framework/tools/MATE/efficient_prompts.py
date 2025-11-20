"""
Token Efficient Tools

Demonstrates TOKEN EFFICIENCY principle:
- Focused prompts
- No unnecessary context
- Specific output requirements
"""
import json
from ..registry import register_tool
from ...core.context import ActionContext
from ...utils.llm import Prompt


@register_tool(
    tags=["analysis", "efficient"],
    description="Analyze sales data efficiently (minimal tokens)"
)
def analyze_sales_efficient(action_context: ActionContext,
                           sales_data: str) -> dict:
    """
    Analyze sales data EFFICIENTLY.
    
    Demonstrates TOKEN EFFICIENCY:
    - Request ONLY what we need
    - Use concise prompts
    - Structured output format
    
    Args:
        action_context: Context with LLM
        sales_data: Sales data to analyze
        
    Returns:
        Focused analysis results
    """
    fast_llm = action_context.get_llm("fast")
    
    if not fast_llm:
        raise ValueError("LLM not available")
    
    schema = {
        "type": "object",
        "properties": {
            "yoy_growth": {"type": "number"},
            "top_3_trends": {
                "type": "array",
                "items": {"type": "string"}
            },
            "anomalies": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
    
    # EFFICIENT PROMPT: Minimal words, specific request
    prompt = f"""Sales Data: {sales_data}

Calculate:
1. YoY growth (%)
2. Top 3 trends
3. Significant anomalies

Return JSON only."""
    
    response = fast_llm(Prompt(messages=[
        {"role": "system", "content": "Respond with only JSON, no extra text"},
        {"role": "user", "content": prompt}
    ]))
    
    try:
        if "```json" in response:
            start = response.find("```json")
            end = response.rfind("```")
            response = response[start+7:end].strip()
        return json.loads(response)
    except:
        return {
            "yoy_growth": 0,
            "top_3_trends": [],
            "anomalies": []
        }


@register_tool(
    tags=["measurement", "efficient"],
    description="Measure prompt token efficiency"
)
def measure_prompt_efficiency(action_context: ActionContext,
                             prompt1: str,
                             prompt2: str) -> dict:
    """
    Compare two prompts to see which is more token efficient.
    
    Demonstrates TOKEN EFFICIENCY analysis.
    
    Args:
        action_context: Context
        prompt1: First prompt
        prompt2: Second prompt
        
    Returns:
        Efficiency comparison
    """
    # Estimate tokens (rough: ~4 chars per token)
    tokens1 = len(prompt1) // 4
    tokens2 = len(prompt2) // 4
    
    # Calculate efficiency
    if tokens1 > 0:
        efficiency = (1 - tokens2 / tokens1) * 100
    else:
        efficiency = 0
    
    return {
        "prompt1_tokens": tokens1,
        "prompt2_tokens": tokens2,
        "savings_percentage": efficiency,
        "more_efficient": "prompt2" if tokens2 < tokens1 else "prompt1",
        "recommendation": {
            "verbose": "Use prompt2 (shorter, same result)",
            "efficient": "Both are good"
        } if efficiency > 10 else "Both are reasonable"
    }


class EfficientPromptBuilder:
    """Helper to build efficient prompts."""
    
    def __init__(self):
        self.parts = []
    
    def add_context(self, context: str) -> 'EfficientPromptBuilder':
        """Add only essential context."""
        self.parts.append(context)
        return self
    
    def add_instruction(self, instruction: str) -> 'EfficientPromptBuilder':
        """Add specific instruction."""
        self.parts.append(f"Instruction: {instruction}")
        return self
    
    def add_format(self, format_spec: str) -> 'EfficientPromptBuilder':
        """Specify output format."""
        self.parts.append(f"Format: {format_spec}")
        return self
    
    def build(self) -> str:
        """Build the final prompt."""
        return "\n\n".join(self.parts)
    
    def count_tokens(self) -> int:
        """Estimate token count."""
        prompt = self.build()
        return len(prompt) // 4  # Rough estimate


# Example usage
def example_efficient_prompt():
    builder = EfficientPromptBuilder()
    
    # Build efficiently
    prompt = (builder
              .add_context("Data: [sales figures]")
              .add_instruction("Calculate YoY growth")
              .add_format("JSON with key 'growth'")
              .build())
    
    # This is much shorter than a verbose prompt!
    return prompt