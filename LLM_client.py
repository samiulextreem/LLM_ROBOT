import os
from dotenv import load_dotenv
from pathlib import Path
import sys
from typing import Optional

class APIClientManager:
    def __init__(self):
        """Initialize the API client manager."""
        self.env_vars = self.load_environment_variables()
        self.initialize_clients()

    def load_environment_variables(self) -> dict:
        """Load environment variables from .env file and return as dictionary."""
        try:
            env_path = self.find_env_file()
            if not env_path:
                raise FileNotFoundError("No .env file found in current or parent directories")
            
            load_dotenv(env_path)
            
            required_vars = [
                'API_KEY',
                # Add other required variables here
            ]
            
            env_vars = {}
            missing_vars = []
            
            for var in required_vars:
                value = os.getenv(var)
                if value is None:
                    missing_vars.append(var)
                else:
                    env_vars[var] = value
                    
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
                
            return env_vars
            
        except Exception as e:
            print(f"Error loading environment variables: {str(e)}")
            sys.exit(1)

    @staticmethod
    def find_env_file(max_depth: int = 3) -> Optional[Path]:
        """Search for .env file in current and parent directories."""
        current = Path.cwd()
        for _ in range(max_depth):
            env_file = current / '.env'
            if env_file.exists():
                return env_file
            current = current.parent
        return None

    def initialize_clients(self):
        """Initialize API clients with environment variables."""
        try:
            # Initialize your clients here using self.env_vars
            # Example:
            # self.client = YourAPIClient(api_key=self.env_vars['API_KEY'])
            pass
            
        except Exception as e:
            print(f"Error initializing clients: {str(e)}")
            sys.exit(1)


client_manager = APIClientManager()
