from typing import Dict, Any, Optional
import json
import os

class Storage:
    """
    Simple persistent storage for agent data.
    Data persists across agent runs.
    """
    
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.data: Dict[str, Dict[str, Any]] = {}
        self.load()
    
    def load(self):
        """Load storage from disk if it exists"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    self.data = json.load(f)
                print(f"[STORAGE] Loaded {len(self.data)} collections from {self.storage_path}")
            except Exception as e:
                print(f"[STORAGE] Error loading storage: {e}")
                self.data = {}
        else:
            print(f"[STORAGE] No existing storage found, starting fresh")
    
    def save(self):
        """Save storage to disk"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            print(f"[STORAGE] Saved {len(self.data)} collections to {self.storage_path}")
        except Exception as e:
            print(f"[STORAGE] Error saving storage: {e}")
    
    def get_collection(self, collection_name: str) -> Dict[str, Any]:
        """Get a storage collection (like a table)"""
        if collection_name not in self.data:
            self.data[collection_name] = {}
        return self.data[collection_name]
    
    def set_in_collection(self, collection_name: str, key: str, value: Any):
        """Store a value in a collection"""
        collection = self.get_collection(collection_name)
        collection[key] = value
        self.save()
    
    def get_from_collection(self, collection_name: str, key: str) -> Optional[Any]:
        """Retrieve a value from a collection"""
        collection = self.get_collection(collection_name)
        return collection.get(key)
    
    def delete_from_collection(self, collection_name: str, key: str) -> bool:
        """Delete a value from a collection"""
        collection = self.get_collection(collection_name)
        if key in collection:
            del collection[key]
            self.save()
            return True
        return False
    
    def list_collection(self, collection_name: str) -> Dict[str, Any]:
        """List all items in a collection"""
        return self.get_collection(collection_name)
    
    def clear_collection(self, collection_name: str):
        """Clear all items in a collection"""
        if collection_name in self.data:
            self.data[collection_name] = {}
            self.save()
    
    def clear_all(self):
        """Clear all storage"""
        self.data = {}
        self.save()