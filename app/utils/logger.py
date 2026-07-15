"""
Logger utility - Simple loguru wrapper
"""
from loguru import logger
import sys

def get_logger(name: str = "app"):
    """Get a logger instance."""
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )
    return logger

__all__ = ["get_logger"]