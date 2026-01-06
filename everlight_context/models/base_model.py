"""
base_model.py

Base model class for EverLight Aetherius Archive.
Provides foundation for all model implementations with mythic theming.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json


class BaseAetheriusModel(ABC):
    """
    Base class for all Aetherius Archive models.
    
    This foundational class provides the interface that all Archive models
    must implement, ensuring consistency across the Omniversal vault.
    """
    
    def __init__(self, model_name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Aetherius model.
        
        Args:
            model_name: Name of the model, honoring Archive conventions
            config: Optional configuration dictionary for model parameters
        """
        self.model_name = model_name
        self.config = config or {}
        self._initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the model and load necessary resources.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Process input data through the model.
        
        Args:
            input_data: Input to be processed by the model
            
        Returns:
            Processed output from the model
        """
        pass
    
    def get_config(self) -> Dict[str, Any]:
        """
        Retrieve the current model configuration.
        
        Returns:
            Dictionary containing model configuration
        """
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        Update model configuration with new parameters.
        
        Args:
            new_config: Dictionary of configuration parameters to update
        """
        self.config.update(new_config)
    
    def save_config(self, filepath: str) -> None:
        """
        Save model configuration to a JSON file.
        
        Args:
            filepath: Path where configuration should be saved
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'model_name': self.model_name,
                'config': self.config
            }, f, indent=2)
    
    @classmethod
    def load_config(cls, filepath: str) -> Dict[str, Any]:
        """
        Load model configuration from a JSON file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            Dictionary containing loaded configuration
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def is_initialized(self) -> bool:
        """
        Check if the model has been initialized.
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return self._initialized
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.model_name}')"
