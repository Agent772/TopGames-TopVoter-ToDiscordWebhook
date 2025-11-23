"""
Configuration module for TopGames TopVoter Discord Webhook.

This module loads and manages configuration from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to manage environment variables."""

    def __init__(self):
        """Initialize configuration from environment variables."""
        self.api_url = os.getenv('API_URL', '')
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL', '')
        self.embed_color = int(os.getenv('EMBED_COLOR', '3447003'))  # Discord blue by default
        self.embed_title = os.getenv('EMBED_TITLE', 'Top Voters')
        self.embed_description = os.getenv('EMBED_DESCRIPTION', 'Here are the top voters!')
        self.max_voters = int(os.getenv('MAX_VOTERS', '10'))

    def validate(self):
        """
        Validate that required configuration is present.

        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        if not self.api_url:
            return False, "API_URL is not set in environment variables"

        if not self.webhook_url:
            return False, "DISCORD_WEBHOOK_URL is not set in environment variables"

        return True, ""


def get_config():
    """
    Get and validate configuration.

    Returns:
        Config: Configuration object

    Raises:
        ValueError: If configuration is invalid
    """
    config = Config()
    is_valid, error_message = config.validate()

    if not is_valid:
        raise ValueError(f"Configuration error: {error_message}")

    return config
