#!/usr/bin/env python3
"""
Main entry point for TopGames TopVoter Discord Webhook.

This script fetches top voters from TopGames API and posts them to Discord.
"""

import sys
import logging
from config import get_config
from api_client import fetch_top_voters
from ranking import get_top_rankings
from webhook import DiscordWebhook

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to orchestrate the workflow."""
    try:
        # Load and validate configuration
        logger.info("Loading configuration...")
        config = get_config()
        logger.info("Configuration loaded successfully")

        # Fetch data from API
        logger.info(f"Fetching voter data from API: {config.api_url}")
        api_data = fetch_top_voters(config.api_url)
        logger.info(f"API response received with code: {api_data.get('code', 'N/A')}")

        # Process and rank players
        logger.info("Processing and ranking players...")
        top_players = get_top_rankings(api_data, config.max_voters)
        logger.info(f"Found {len(top_players)} top voters")

        if not top_players:
            logger.warning("No valid players found in API response")
        else:
            # Log top players for verification
            for player in top_players[:3]:  # Show top 3 in logs
                logger.info(
                    f"  {player['rank']}. {player['playername']}: {player['votes']} votes"
                )

        # Send to Discord
        logger.info("Sending rankings to Discord webhook...")
        webhook = DiscordWebhook(config.webhook_url)
        success = webhook.send_rankings(
            top_players,
            config.embed_title,
            config.embed_description,
            config.embed_color
        )

        if success:
            logger.info("Successfully sent rankings to Discord!")
            return 0
        else:
            logger.error("Failed to send rankings to Discord")
            return 1

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
