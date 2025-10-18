"""
Financial Portfolio Scanner - Settings Configuration

This module contains configuration settings for the financial portfolio monitoring system.
"""

import os
import logging
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Configuration settings for the financial portfolio scanner.
    """
    
    # OpenAI API Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_CHAT_MODEL_ID: str = os.getenv("OPENAI_CHAT_MODEL_ID", "gpt-4o")
    
    # Application Configuration
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "true").lower() == "true"
        
    # Portfolio Configuration
    PORTFOLIO_UPDATE_INTERVAL: int = int(os.getenv("PORTFOLIO_UPDATE_INTERVAL", "3600"))  # seconds
    
    # Reporting Configuration
    REPORT_FORMAT: str = os.getenv("REPORT_FORMAT", "pdf")
    REPORT_OUTPUT_DIR: str = os.getenv("REPORT_OUTPUT_DIR", "./reports")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "portfolio_scanner.log")
    
    # Optional Financial Data API Keys
    FINNHUB_API_KEY: Optional[str] = os.getenv("FINNHUB_API_KEY")
    BLOOMBERG_API_KEY: Optional[str] = os.getenv("BLOOMBERG_API_KEY")
    FACTSET_API_KEY: Optional[str] = os.getenv("FACTSET_API_KEY")
    
    # API Configuration
    API_KEY: Optional[str] = os.getenv("API_KEY")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.example.com")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///portfolio_scanner.db")
    
    @classmethod
    def validate_settings(cls) -> bool:
        """
        Validate that all required settings are properly configured.
        
        Returns:
            bool: True if all settings are valid, False otherwise
            
        Raises:
            ValueError: If required configuration values are missing or invalid
        """
        errors = []
        
        # Validate OpenAI API configuration
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required but not set")
        
        # Validate API configuration
        if not cls.API_KEY:
            errors.append("API_KEY is required but not set")
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if cls.LOG_LEVEL not in valid_log_levels:
            errors.append(f"LOG_LEVEL must be one of {valid_log_levels}, got '{cls.LOG_LEVEL}'")
        
        # Validate portfolio update interval
        if cls.PORTFOLIO_UPDATE_INTERVAL <= 0:
            errors.append("PORTFOLIO_UPDATE_INTERVAL must be a positive integer")
        
        # Validate report format
        valid_report_formats = ["pdf", "html", "json", "csv"]
        if cls.REPORT_FORMAT.lower() not in valid_report_formats:
            errors.append(f"REPORT_FORMAT must be one of {valid_report_formats}, got '{cls.REPORT_FORMAT}'")
        
        # Validate API base URL
        if not cls.API_BASE_URL or not cls.API_BASE_URL.strip():
            errors.append("API_BASE_URL cannot be empty or contain only whitespace")
        
        # Validate database URL
        if not cls.DATABASE_URL or not cls.DATABASE_URL.strip():
            errors.append("DATABASE_URL cannot be empty or contain only whitespace")
        
        # Validate report output directory
        if not cls.REPORT_OUTPUT_DIR or not cls.REPORT_OUTPUT_DIR.strip():
            errors.append("REPORT_OUTPUT_DIR cannot be empty or contain only whitespace")
        
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        return True
    
    @classmethod
    def get_logging_config(cls) -> Dict[str, Any]:
        """
        Get the logging configuration based on current settings.
        
        Returns:
            Dict[str, Any]: Dictionary with logging configuration
            
        Raises:
            ValueError: If LOG_LEVEL is invalid
        """
        try:
            log_level = getattr(logging, cls.LOG_LEVEL.upper())
        except AttributeError:
            valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            error_msg = f"Invalid LOG_LEVEL: '{cls.LOG_LEVEL}'. Must be one of {valid_log_levels}"
            logging.error(error_msg)
            raise ValueError(error_msg)
            
        return {
            "level": log_level,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "filename": cls.LOG_FILE if cls.LOG_FILE else None,
            "filemode": "a"
        }
    
    @classmethod
    def get_openai_config(cls) -> Dict[str, str]:
        """
        Get the OpenAI configuration.
        
        Returns:
            Dict[str, str]: Dictionary with OpenAI configuration
            
        Raises:
            ValueError: If OPENAI_API_KEY is empty or contains only whitespace
        """
        if not cls.OPENAI_API_KEY or not cls.OPENAI_API_KEY.strip():
            error_msg = "OPENAI_API_KEY cannot be empty or contain only whitespace"
            logging.error(error_msg)
            raise ValueError(error_msg)
            
        if not cls.OPENAI_CHAT_MODEL_ID or not cls.OPENAI_CHAT_MODEL_ID.strip():
            error_msg = "OPENAI_CHAT_MODEL_ID cannot be empty or contain only whitespace"
            logging.error(error_msg)
            raise ValueError(error_msg)
            
        return {
            "api_key": cls.OPENAI_API_KEY,
            "model": cls.OPENAI_CHAT_MODEL_ID
        }