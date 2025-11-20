from typing import Any, Dict, Callable

class ActionContext:
    """
    Context object passed to tools that need access to shared resources
    like the LLM, agent state, storage, or configuration.
    """
    def __init__(self, 
                 llm: Callable = None,
                 fast_llm: Callable = None,        # ← Small, quick model
                 powerful_llm: Callable = None,    # ← Larger, more powerful model
                 agent: Any = None,
                 memory: Any = None,
                 storage: Any = None,
                 metadata: Dict = None):
        """
        Initialize the action context.
        
        Args:
            llm: Function to call the LLM (generate_response)
            agent: Reference to the agent instance
            memory: Reference to the agent's memory
            storage: Reference to persistent storage
            metadata: Additional contextual information
        """
        self._context = {
            "llm": llm or fast_llm,          # Default to fast model
            "fast_llm": fast_llm,            # Small & cheap
            "powerful_llm": powerful_llm,    # Large & expensive
            "agent": agent,
            "memory": memory,
            "storage": storage,
            "metadata": metadata or {}
        }
    
    def get(self, key: str, default=None):
        """Get a value from the context"""
        return self._context.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a value in the context"""
        self._context[key] = value
    
    def get_llm(self, model_type: str = "fast") -> Callable:
        """
        Get an LLM model by type.
        
        Args:
            model_type: "fast", "powerful", or "default"
            
        Returns:
            The requested LLM function
        """
        if model_type == "fast":
            return self._context.get("fast_llm")
        elif model_type == "powerful":
            return self._context.get("powerful_llm")
        else:
            return self._context.get("llm")
    
    def get_agent(self):
        """Convenience method to get the agent"""
        return self._context.get("agent")
    
    def get_memory(self):
        """Convenience method to get the memory"""
        return self._context.get("memory")
    
    def get_storage(self):
        """Convenience method to get the storage"""
        return self._context.get("storage")