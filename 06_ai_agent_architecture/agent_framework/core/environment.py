import time
import traceback
from typing import Any
from .action import Action
from .context import ActionContext

class Environment:
    def __init__(self):
        self.action_context = None
    
    def set_context(self, action_context: ActionContext):
        """Set the action context for this environment"""
        self.action_context = action_context
    
    def execute_action(self, action: Action, args: dict) -> dict:
        """Execute an action and return the result."""
        try:
            # Pass context if action requires it
            if action.requires_context:
                result = action.execute(action_context=self.action_context, **args)
            else:
                result = action.execute(**args)
            
            return self.format_result(result)
        except Exception as e:
            return {
                "tool_executed": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
    
    def format_result(self, result: Any) -> dict:
        """Format the result with metadata."""
        return {
            "tool_executed": True,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")
        }