"""
Reversible Action System

Implements ENVIRONMENTAL SAFETY principle:
- All actions can be undone
- Transactions are atomic (all or nothing)
- Changes can be staged for review
"""
from typing import Callable, Any, Dict, List
from datetime import datetime
import uuid
import json


class ReversibleAction:
    """
    An action that can be undone.
    
    Stores enough information to reverse the operation.
    """
    
    def __init__(self, 
                 name: str,
                 execute_func: Callable,
                 reverse_func: Callable,
                 description: str = ""):
        """
        Initialize a reversible action.
        
        Args:
            name: Action identifier
            execute_func: Function to execute the action
            reverse_func: Function to reverse/undo the action
            description: Human-readable description
        """
        self.name = name
        self.execute = execute_func
        self.reverse = reverse_func
        self.description = description
        self.execution_record: Dict[str, Any] = None
        self.execution_id: str = None
    
    def run(self, **args) -> Any:
        """
        Execute action and record how to reverse it.
        
        Args:
            **args: Arguments for the action
            
        Returns:
            Result of executing the action
        """
        # Generate execution ID for this run
        self.execution_id = str(uuid.uuid4())
        
        # Execute the action
        result = self.execute(**args)
        
        # Record execution details for reversal
        self.execution_record = {
            "action_name": self.name,
            "execution_id": self.execution_id,
            "timestamp": datetime.now().isoformat(),
            "args": args,
            "result": result
        }
        
        print(f"[Action Executed] {self.name} (ID: {self.execution_id})")
        
        return result
    
    def undo(self) -> Any:
        """
        Reverse the action using recorded information.
        
        Returns:
            Result of reversing the action
            
        Raises:
            ValueError: If no action was executed
        """
        if not self.execution_record:
            raise ValueError(f"Cannot undo {self.name}: No execution record")
        
        # Call reverse function with recorded info
        result = self.reverse(**self.execution_record)
        
        print(f"[Action Reversed] {self.name} (ID: {self.execution_id})")
        
        return result


class ActionTransaction:
    """
    Group multiple actions into an atomic transaction.
    
    Either ALL actions execute, or NONE of them do (with rollback).
    """
    
    def __init__(self):
        """Initialize a transaction."""
        self.transaction_id = str(uuid.uuid4())
        self.actions: List[tuple] = []  # List of (action, args)
        self.executed: List[ReversibleAction] = []  # Successfully executed actions
        self.committed = False
        self.creation_time = datetime.now()
    
    def add(self, action: ReversibleAction, **args):
        """
        Queue an action for execution.
        
        Args:
            action: ReversibleAction to queue
            **args: Arguments for the action
            
        Raises:
            ValueError: If transaction already committed
        """
        if self.committed:
            raise ValueError("Cannot add actions to committed transaction")
        
        self.actions.append((action, args))
        print(f"[Queued] {action.name} in transaction {self.transaction_id}")
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute all actions in the transaction.
        
        If ANY action fails, automatically rolls back all previous actions.
        
        Returns:
            Dictionary with execution results
            
        Raises:
            Exception: If any action fails (after rollback)
        """
        print(f"\n[Transaction] Executing {len(self.actions)} actions...")
        
        try:
            results = []
            
            # Execute each action in order
            for action, args in self.actions:
                result = action.run(**args)
                results.append(result)
                self.executed.append(action)  # Track for rollback
            
            print(f"[Transaction] All {len(self.actions)} actions succeeded ✓")
            
            return {
                "status": "success",
                "transaction_id": self.transaction_id,
                "actions_executed": len(self.actions),
                "results": results
            }
        
        except Exception as e:
            print(f"\n[Transaction FAILED] Rolling back all actions...")
            print(f"Error: {str(e)}\n")
            
            # Roll back in reverse order
            self.rollback()
            
            raise Exception(f"Transaction failed: {str(e)}") from e
    
    def rollback(self):
        """
        Reverse all executed actions in reverse order.
        
        Critical for maintaining consistency.
        """
        print(f"[Rollback] Reversing {len(self.executed)} actions...")
        
        # Reverse order: undo last action first
        for action in reversed(self.executed):
            try:
                action.undo()
            except Exception as e:
                print(f"[Rollback ERROR] Failed to undo {action.name}: {str(e)}")
        
        self.executed = []
        print(f"[Rollback] Complete")
    def commit(self):
        """
        Mark transaction as committed (prevent new actions).
        """
        self.committed = True
        print(f"[Transaction] Committed: {self.transaction_id}")

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the transaction."""
        return {
            "transaction_id": self.transaction_id,
            "status": "committed" if self.committed else "pending",
            "actions_queued": len(self.actions),
            "actions_executed": len(self.executed),
            "creation_time": self.creation_time.isoformat(),
            "action_names": [action.name for action, _ in self.actions]
        }

class StagedActionEnvironment:
    """
    Environment that stages actions for review before execution.
    
    Allows human or AI review before executing actions.
    """
    
    def __init__(self, llm=None):
        """
        Initialize staged environment.
        
        Args:
            llm: Optional LLM for automated review
        """
        self.staged_transactions: Dict[str, ActionTransaction] = {}
        self.llm = llm
    
    def create_transaction(self) -> ActionTransaction:
        """
        Create a new transaction for staging actions.
        
        Returns:
            New ActionTransaction instance
        """
        transaction = ActionTransaction()
        self.staged_transactions[transaction.transaction_id] = transaction
        return transaction
    
    def stage_action(self, transaction_id: str, 
                    action: ReversibleAction, 
                    **args):
        """
        Add an action to a staged transaction.
        
        Args:
            transaction_id: Transaction to add to
            action: Action to stage
            **args: Arguments for the action
        """
        if transaction_id not in self.staged_transactions:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        transaction = self.staged_transactions[transaction_id]
        transaction.add(action, **args)
    
    def review_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Review staged actions for safety.
        
        Returns:            Review results with approval status
        """
        if transaction_id not in self.staged_transactions:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        transaction = self.staged_transactions[transaction_id]
        
        # Create human-readable description
        staged_actions = []
        for action, args in transaction.actions:
            staged_actions.append({
                "action": action.name,
                "description": action.description,
                "arguments": args
            })
        
        review_summary = {
            "transaction_id": transaction_id,
            "staged_actions": staged_actions,
            "action_count": len(staged_actions),
            "review_items": []
        }
        
        # Add safety considerations
        for i, (action, args) in enumerate(transaction.actions, 1):
            review_summary["review_items"].append({
                "step": i,
                "action": action.name,
                "safety_questions": [
                    "Is this action necessary?",
                    "Could this have unintended consequences?",
                    "Is the order correct?",
                    "Are arguments valid?",
                    "Does user have permission?"
                ]
            })
        
        return review_summary
    
    def approve_and_execute(self, transaction_id: str) -> Dict[str, Any]:
        """
        Approve and execute staged transaction.
        
        Args:
            transaction_id: Transaction to execute
            
        Returns:
            Execution results
        """
        if transaction_id not in self.staged_transactions:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        transaction = self.staged_transactions[transaction_id]
        
        # Execute the transaction
        result = transaction.execute()
        
        # Mark as committed
        transaction.commit()
        
        return result
    
    def reject_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Reject a staged transaction (don't execute).
        
        Args:
            transaction_id: Transaction to reject
            
        Returns:
            Rejection confirmation
        """
        if transaction_id not in self.staged_transactions:
            raise ValueError(f"Transaction {transaction_id} not found")
        
        transaction = self.staged_transactions[transaction_id]
        
        print(f"[Transaction Rejected] {transaction_id}")
        
        return {
            "status": "rejected",
            "transaction_id": transaction_id,
            "message": f"Staged transaction with {len(transaction.actions)} actions was rejected"
        }