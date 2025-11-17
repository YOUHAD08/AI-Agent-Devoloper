import json
from typing import Dict
from .registry import register_tool
from ..core.context import ActionContext
from ..utils.llm import Prompt

@register_tool(
    tags=["llm", "extraction"],
    description="Have the LLM generate JSON in response to a prompt. Use this when you need structured data extraction."
)
def prompt_llm_for_json(action_context: ActionContext, schema: dict, prompt: str) -> dict:
    """
    Have the LLM generate JSON in response to a prompt.
    
    Args:
        action_context: Context containing LLM and other resources
        schema: JSON schema defining the expected structure
        prompt: The prompt to send to the LLM
        
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
                    "content": f"You MUST produce output that adheres to the following JSON schema:\n\n{json.dumps(schema, indent=4)}. Output your JSON in a ```json markdown block."
                },
                {"role": "user", "content": prompt}
            ]))

            # Check if the response has json inside of a markdown code block
            if "```json" in response:
                # Search from the front and then the back
                start = response.find("```json")
                end = response.rfind("```")
                response = response[start+7:end].strip()

            # Parse and validate the JSON response
            return json.loads(response)
            
        except Exception as e:
            if i == 2:  # On last try, raise the error
                raise e
            print(f"Error generating JSON: {e}")
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
            "content": f"You are an expert in {domain}. Provide professional, detailed analysis."
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
            "content": "You are a text transformation specialist. Follow instructions precisely."
        },
        {
            "role": "user",
            "content": f"Transform the following text:\n\n{text}\n\nTransformation requested: {transformation}"
        }
    ]))
    
    return response