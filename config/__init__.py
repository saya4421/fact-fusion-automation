"""
Fact Fusion Automation - Config Module
"""

import toml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Load settings from settings.toml
settings_path = Path(__file__).parent / "settings.toml"
settings = toml.load(settings_path)

# Export settings for easy import
__all__ = ["settings"]