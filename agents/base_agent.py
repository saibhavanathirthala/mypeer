"""
Base Agent class for the AI Pair Programming multi-agent framework.
All agents inherit from this base class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for all agents in the framework."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the base agent.
        
        Args:
            name: Name of the agent
            config: Configuration dictionary for the agent
        """
        self.name = name
        self.config = config or {}
    
    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Execute the agent's main functionality.
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            Processed output from the agent
        """
        pass
    
    def log(self, message: str) -> None:
        """Log a message with the agent's name."""
        print(f"[{self.name}] {message}")
