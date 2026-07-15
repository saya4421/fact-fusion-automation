"""
App Config - Re-export from root config
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings as config

__all__ = ["config"]