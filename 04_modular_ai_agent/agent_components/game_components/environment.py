import time
import traceback
from .action import Action


class Environment:
  def execute_action(self, action: Action, args: dict) -> dict:
    """Execute an action in the environment and return the result."""
    try:
      result = action.execute(**args)
      return self._format_result(result)
    except Exception as e:
      return {
        "tool_executed": False,
        "error": str(e),
        "traceback": traceback.format_exc()
      }
    
  def _format_result(self, result: any) -> dict:
    """Format the result of an action execution."""
    return {
      "tool_executed": True,
      "result": result,
      "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }