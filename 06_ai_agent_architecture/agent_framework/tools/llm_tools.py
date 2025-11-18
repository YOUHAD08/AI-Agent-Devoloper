import json
from typing import Dict
from .registry import register_tool
from ..core.context import ActionContext
from ..utils.llm import Prompt

# Add this to the existing llm_tools.py file

@register_tool(
    tags=["llm", "expert"],
    description="Consult an expert persona for specialized knowledge and analysis."
)
def prompt_expert(action_context: ActionContext, 
                  description_of_expert: str, 
                  prompt: str) -> str:
    """
    Consult an expert persona for specialized analysis.
    
    This implements the PERSONA PATTERN:
    - Act as [EXPERT X]
    - Perform [TASK Y]
    
    Args:
        action_context: Context containing LLM
        description_of_expert: Description of the expert persona 
                              (e.g., "A senior financial analyst with expertise in...")
        prompt: The question or task for the expert
        
    Returns:
        Expert's response as a string
    """
    generate_response = action_context.get_llm()
    
    if not generate_response:
        raise ValueError("LLM not available in action context")
    
    # Construct persona-based prompt
    system_message = f"You are {description_of_expert}. Provide expert analysis based on your specialized knowledge and experience."
    
    response = generate_response(Prompt(messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]))
    
    return response


@register_tool(
    tags=["llm", "expert", "structured"],
    description="Consult an expert and get structured JSON response."
)
def prompt_expert_for_json(action_context: ActionContext,
                           description_of_expert: str,
                           prompt: str,
                           schema: dict) -> dict:
    """
    Consult an expert persona and get structured JSON output.
    
    Combines PERSONA PATTERN with structured output.
    
    Args:
        action_context: Context containing LLM
        description_of_expert: Description of the expert persona
        prompt: The question or task for the expert
        schema: JSON schema for the expected response
        
    Returns:
        Structured response as a dictionary
    """
    generate_response = action_context.get_llm()
    
    if not generate_response:
        raise ValueError("LLM not available in action context")
    
    # Construct persona-based prompt with schema requirement
    system_message = f"""You are {description_of_expert}. 
Provide expert analysis based on your specialized knowledge and experience.

You MUST respond with JSON that adheres to this schema:
{json.dumps(schema, indent=2)}

Output your JSON in a ```json markdown block."""
    
    # Try up to 3 times
    for i in range(3):
        try:
            response = generate_response(Prompt(messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]))
            
            # Extract JSON
            if "```json" in response:
                start = response.find("```json")
                end = response.rfind("```")
                response = response[start+7:end].strip()
            
            return json.loads(response)
            
        except Exception as e:
            if i == 2:
                raise e
            print(f"Error generating expert response: {e}")
            print("Retrying...")

def validate_json_schema(data: dict, schema: dict) -> tuple[bool, list]:
    """
    Simple JSON schema validator.
    Returns (is_valid, errors)
    """
    errors = []
    
    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Check property types
    properties = schema.get("properties", {})
    for key, value in data.items():
        if key in properties:
            expected_type = properties[key].get("type")
            actual_type = type(value).__name__
            
            # Map Python types to JSON schema types
            type_map = {
                "str": "string",
                "int": "integer",
                "float": "number",
                "bool": "boolean",
                "list": "array",
                "dict": "object"
            }
            
            if type_map.get(actual_type) != expected_type:
                errors.append(f"Field '{key}' has wrong type: expected {expected_type}, got {actual_type}")
    
    return len(errors) == 0, errors


@register_tool(
    tags=["llm", "extraction"],
    description="Have the LLM generate JSON in response to a prompt. Use this when you need structured data extraction."
)
def prompt_llm_for_json(action_context: ActionContext, schema: dict, prompt: str, validate: bool = True) -> dict:
    """
    Have the LLM generate JSON in response to a prompt.
    
    Args:
        action_context: Context containing LLM and other resources
        schema: JSON schema defining the expected structure
        prompt: The prompt to send to the LLM
        validate: Whether to validate the result against the schema
        
    Returns:
        A dictionary matching the provided schema with extracted information
    """
    generate_response = action_context.get_llm()
    
    if not generate_response:
        raise ValueError("LLM not available in action context")
    
    # Try up to 3 times to get valid JSON
    for i in range(3):
        try:
            # Send prompt with schema instruction and get response
            response = generate_response(Prompt(messages=[
                {
                    "role": "system", 
                    "content": f"You MUST produce output that adheres to the following JSON schema:\n\n{json.dumps(schema, indent=4)}.\n\nIMPORTANT: Output your JSON in a ```json markdown block."
                },
                {"role": "user", "content": prompt}
            ]))

            # Check if the response has json inside of a markdown code block
            if "```json" in response:
                # Search from the front and then the back
                start = response.find("```json")
                end = response.rfind("```")
                response = response[start+7:end].strip()

            # Parse the JSON response
            result = json.loads(response)
            
            # Validate if requested
            if validate:
                is_valid, validation_errors = validate_json_schema(result, schema)
                if not is_valid:
                    error_msg = f"Schema validation failed: {', '.join(validation_errors)}"
                    if i == 2:  # Last attempt
                        raise ValueError(error_msg)
                    print(f"Validation error: {error_msg}")
                    print("Retrying...")
                    continue
            
            return result
            
        except json.JSONDecodeError as e:
            if i == 2:  # On last try, raise the error
                raise ValueError(f"Failed to parse JSON after 3 attempts: {e}")
            print(f"Error parsing JSON: {e}")
            print("Retrying...")
        except Exception as e:
            if i == 2:  # On last try, raise the error
                raise e
            print(f"Error generating response: {e}")
            print("Retrying...")


@register_tool(
    tags=["llm", "analysis"],
    description="Analyze text using the LLM as a domain expert."
)
def analyze_as_expert(action_context: ActionContext, domain: str, text: str, question: str) -> str:
    """
    Have the LLM analyze text as a domain expert.
    
    Args:
        action_context: Context containing LLM
        domain: The expert domain (e.g., "marketing", "cybersecurity", "finance")
        text: The text to analyze
        question: The specific question or analysis task
        
    Returns:
        Expert analysis as a string
    """
    generate_response = action_context.get_llm()
    
    if not generate_response:
        raise ValueError("LLM not available in action context")
    
    response = generate_response(Prompt(messages=[
        {
            "role": "system",
            "content": f"You are a world-class expert in {domain}. Provide professional, detailed analysis with specific insights and actionable recommendations."
        },
        {
            "role": "user",
            "content": f"Text to analyze:\n{text}\n\nQuestion: {question}"
        }
    ]))
    
    return response


@register_tool(
    tags=["llm", "transformation"],
    description="Transform text into a different format or style using the LLM."
)
def transform_text(action_context: ActionContext, text: str, transformation: str) -> str:
    """
    Transform text using the LLM.
    
    Args:
        action_context: Context containing LLM
        text: The text to transform
        transformation: Description of the desired transformation
        
    Returns:
        Transformed text
    """
    generate_response = action_context.get_llm()
    
    if not generate_response:
        raise ValueError("LLM not available in action context")
    
    response = generate_response(Prompt(messages=[
        {
            "role": "system",
            "content": "You are a text transformation specialist. Follow instructions precisely and output ONLY the transformed text with no preamble or explanation."
        },
        {
            "role": "user",
            "content": f"Transform the following text:\n\n{text}\n\nTransformation requested: {transformation}"
        }
    ]))
    
    return response


@register_tool(
    tags=["llm", "validation"],
    description="Validate if text meets specific criteria using the LLM."
)
def validate_with_llm(action_context: ActionContext, text: str, criteria: str) -> dict:
    """
    Validate text against criteria using the LLM.
    
    Args:
        action_context: Context containing LLM
        text: The text to validate
        criteria: The validation criteria
        
    Returns:
        Dictionary with validation results
    """
    schema = {
        "type": "object",
        "required": ["is_valid", "reasoning"],
        "properties": {
            "is_valid": {"type": "boolean"},
            "reasoning": {"type": "string"},
            "issues": {
                "type": "array",
                "items": {"type": "string"}
            },
            "suggestions": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
    
    prompt = f"""
Validate if the following text meets these criteria:
{criteria}

Text to validate:
{text}

Provide:
- is_valid: true/false
- reasoning: why it passes or fails
- issues: list of specific problems (if any)
- suggestions: how to fix issues (if any)
"""
    
    return prompt_llm_for_json(action_context, schema, prompt)