"""
Model Efficiency Tools

Demonstrates using the right model for the right task.
"""
import json
from ..registry import register_tool
from ...core.context import ActionContext
from ...utils.llm import Prompt


@register_tool(
    tags=["extraction", "efficient"],
    description="Extract structured data using fast, lightweight model"
)
def extract_data_fast(action_context: ActionContext, 
                      data_type: str,
                      text: str) -> dict:
    """
    Extract structured data using a FAST model.
    
    Demonstrates MODEL EFFICIENCY principle:
    Use small models for simple extraction tasks.
    
    Args:
        action_context: Context with model options
        data_type: Type of data to extract (email, phone, name, etc.)
        text: Text to extract from
        
    Returns:
        Extracted data as dictionary
    """
    # Get FAST model for simple extraction
    fast_llm = action_context.get_llm("fast")
    
    if not fast_llm:
        raise ValueError("Fast LLM not available in action context")
    
    schema = {
        "type": "object",
        "properties": {
            "extracted_value": {"type": "string"},
            "confidence": {"type": "number"},
            "found": {"type": "boolean"}
        }
    }
    
    prompt = f"""Extract {data_type} from this text:

Text: "{text}"

Respond with JSON containing:
- extracted_value: the {data_type} found
- confidence: 0.0 to 1.0 confidence level
- found: true if {data_type} was found"""
    
    response = fast_llm(Prompt(messages=[
        {"role": "system", "content": f"Extract {data_type} efficiently. Be concise."},
        {"role": "user", "content": prompt}
    ]))
    
    # Parse JSON
    try:
        if "```json" in response:
            start = response.find("```json")
            end = response.rfind("```")
            response = response[start+7:end].strip()
        return json.loads(response)
    except:
        return {
            "extracted_value": response.strip(),
            "confidence": 0.5,
            "found": True
        }


@register_tool(
    tags=["analysis", "complex"],
    description="Perform complex analysis using powerful model"
)
def analyze_complex(action_context: ActionContext,
                    analysis_type: str,
                    content: str,
                    depth: str = "detailed") -> dict:
    """
    Perform complex analysis using a POWERFUL model.
    
    Demonstrates MODEL EFFICIENCY principle:
    Use powerful models for complex reasoning tasks.
    
    Args:
        action_context: Context with model options
        analysis_type: Type of analysis needed
        content: Content to analyze
        depth: Level of analysis (quick, standard, detailed)
        
    Returns:
        Analysis result as dictionary
    """
    # Get POWERFUL model for complex analysis
    powerful_llm = action_context.get_llm("powerful")
    
    if not powerful_llm:
        raise ValueError("Powerful LLM not available in action context")
    
    schema = {
        "type": "object",
        "properties": {
            "analysis": {"type": "string"},
            "key_findings": {
                "type": "array",
                "items": {"type": "string"}
            },
            "potential_issues": {
                "type": "array",
                "items": {"type": "string"}
            },
            "recommendations": {
                "type": "array",
                "items": {"type": "string"}
            },
            "confidence": {"type": "number"}
        }
    }
    
    depth_instructions = {
        "quick": "Provide 2-3 key findings",
        "standard": "Provide 4-5 findings with brief explanations",
        "detailed": "Provide comprehensive analysis with all details"
    }
    
    prompt = f"""Perform {analysis_type} analysis with {depth} depth.

{depth_instructions.get(depth, 'Provide standard analysis')}

Content to analyze:
{content}

Identify:
1. Key findings
2. Potential issues or contradictions
3. Recommendations"""
    
    response = powerful_llm(Prompt(messages=[
        {"role": "system", "content": f"You are an expert at {analysis_type} analysis. Provide thorough, accurate analysis."},
        {"role": "user", "content": prompt}
    ]))
    
    # Parse response (would use prompt_llm_for_json in real implementation)
    return {
        "analysis": response,
        "key_findings": [],
        "potential_issues": [],
        "recommendations": [],
        "confidence": 0.85
    }


@register_tool(
    tags=["routing", "efficient"],
    description="Determine which model to use for a task"
)
def determine_best_model(action_context: ActionContext,
                        task_description: str) -> dict:
    """
    Use fast model to determine if a task needs a powerful model.
    
    This is meta-efficient: Use fast model to route to fast or powerful.
    
    Args:
        action_context: Context with model options
        task_description: Description of the task
        
    Returns:
        Recommendation for which model to use
    """
    fast_llm = action_context.get_llm("fast")
    
    if not fast_llm:
        raise ValueError("Fast LLM not available")
    
    prompt = f"""Analyze this task and recommend which model to use:

Task: {task_description}

Respond with JSON:
{{
    "recommended_model": "fast" or "powerful",
    "reasoning": "why this model",
    "complexity_score": 0-10,
    "estimated_cost_relative": number
}}

Guidelines:
- Simple extraction, formatting, basic classification → "fast"
- Complex reasoning, analysis, synthesis → "powerful"
- Borderline → "fast" (prefer efficiency)"""
    
    response = fast_llm(Prompt(messages=[
        {"role": "system", "content": "You are efficient at task routing."},
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
            "recommended_model": "fast",
            "reasoning": "Default to fast for efficiency",
            "complexity_score": 3,
            "estimated_cost_relative": 1
        }