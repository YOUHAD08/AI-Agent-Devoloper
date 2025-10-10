class Memory:
    def __init__(self):
        self.items = []

    def add_memory(self, memory : dict):
        """Add a memory to working memory."""
        self.items.append(memory)

    def get_memories(self, limit :int = None) -> list[dict]:
        return self.items[:limit] if limit else self.items
    
    def copy_without_system_memories(self):
        """Return a copy of the memory without system memories"""
        filtered_items = [m for m in self.items if m["type"] != "system"]
        memory = Memory()
        memory.items = filtered_items
        return memory

