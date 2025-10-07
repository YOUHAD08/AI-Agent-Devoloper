class Memory:
    def __init__(self):
        self.items = []

    def add_memory(self, memory : dict):
        """Add a memory to working memory."""
        self.items.append(memory)

    def recall(self, limit :int = None) -> list[dict]:
        return self.items[:limit] if limit else self.items

