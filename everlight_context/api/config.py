"""
config.py

API configuration management for external integrations.
"""

from typing import Dict, Any, Optional
import json
import os


class APIConfig:
    """
    Configuration manager for API connections.
    Handles credentials and settings for external services.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize API configuration.
        
        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or environment.
        
        Returns:
            Configuration dictionary
        """
        config = {}
        
        # Try to load from file
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading config file: {e}")
        
        # Override with environment variables
        config.setdefault('nextcloud', {})
        config['nextcloud']['url'] = os.environ.get(
            'NEXTCLOUD_URL',
            config.get('nextcloud', {}).get('url', '')
        )
        config['nextcloud']['username'] = os.environ.get(
            'NEXTCLOUD_USERNAME',
            config.get('nextcloud', {}).get('username', '')
        )
        config['nextcloud']['password'] = os.environ.get(
            'NEXTCLOUD_PASSWORD',
            config.get('nextcloud', {}).get('password', '')
        )
        config['nextcloud']['app_password'] = os.environ.get(
            'NEXTCLOUD_APP_PASSWORD',
            config.get('nextcloud', {}).get('app_password', '')
        )
        
        # MCP server configuration
        config.setdefault('mcp', {})
        config['mcp']['host'] = os.environ.get(
            'MCP_HOST',
            config.get('mcp', {}).get('host', '0.0.0.0')
        )
        config['mcp']['port'] = int(os.environ.get(
            'MCP_PORT',
            config.get('mcp', {}).get('port', 8080)
        ))
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'nextcloud.url')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, filepath: Optional[str] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            filepath: Optional path to save to (uses config_file if not provided)
        """
        save_path = filepath or self.config_file
        
        if not save_path:
            raise ValueError("No file path specified for saving configuration")
        
        # Remove sensitive data before saving
        safe_config = self.config.copy()
        if 'nextcloud' in safe_config:
            safe_config['nextcloud'].pop('password', None)
            safe_config['nextcloud'].pop('app_password', None)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(safe_config, f, indent=2)
    
    def validate_nextcloud_config(self) -> bool:
        """
        Validate Nextcloud configuration.
        
        Returns:
            True if configuration is valid
        """
        nc_config = self.config.get('nextcloud', {})
        
        required_fields = ['url']
        for field in required_fields:
            if not nc_config.get(field):
                return False
        
        # Check for credentials
        has_credentials = (
            (nc_config.get('username') and nc_config.get('password')) or
            nc_config.get('app_password')
        )
        
        return has_credentials
