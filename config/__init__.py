"""
Fact Fusion Automation - Config Module
"""
import os
import toml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded config/.env")

# Load settings from settings.toml
settings_path = Path(__file__).parent / "settings.toml"
settings = toml.load(settings_path)

# Override settings.toml with .env variables if present
env_api_key = os.getenv('OPENAI_API_KEY')
if env_api_key:
    settings['app']['openai_api_key'] = env_api_key
    print(f"✅ API key loaded from .env")

env_base_url = os.getenv('OPENAI_BASE_URL')
if env_base_url:
    settings['app']['openai_base_url'] = env_base_url

env_model = os.getenv('OPENAI_MODEL')
if env_model:
    settings['app']['openai_model_name'] = env_model

# Export settings for easy import
__all__ = ["settings"]