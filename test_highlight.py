#!/usr/bin/env python3
"""
Test script to simulate a month-end final ranking with highlighting.
"""

import sys
import logging
from datetime import datetime
from config import get_config
from api_client import fetch_top_voters
from ranking import get_top_rankings
from webhook import DiscordWebhook
from schedule_manager import ScheduleManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_highlighted_message():
    """Test the highlighted month-end final ranking."""
    try:
        logger.info("🧪 Testing Month-End Final Ranking Highlight")
        logger.info("=" * 50)

        # Load configuration
        config = get_config()
        
        # Simulate last day of month
        test_date = datetime(2025, 11, 30)  # Last day of November (also a Sunday)
        logger.info(f"Simulating date: {test_date.strftime('%A, %B %d, %Y')}")
        
        # Get embed configuration for month-end
        post_type = ScheduleManager.get_post_type(test_date)
        embed_config = ScheduleManager.get_embed_config(post_type)
        
        logger.info(f"Post type: {post_type}")
        logger.info(f"Embed color: {embed_config['color']} (Gold highlight)")
        logger.info(f"Title suffix: '{embed_config['title_suffix']}'")
        
        # Fetch current data
        logger.info("Fetching current voter data...")
        api_data = fetch_top_voters(config.api_url)
        top_players = get_top_rankings(api_data, config.max_voters)
        
        # Prepare highlighted title and description
        title = config.embed_title + embed_config['title_suffix']
        description = embed_config['description_prefix'] + config.embed_description
        color = embed_config['color']
        
        logger.info(f"Final title: '{title}'")
        logger.info(f"Final description: '{description}'")
        
        # Send the highlighted message
        webhook = DiscordWebhook(config.webhook_url)
        logger.info("🎯 Sending highlighted FINAL RANKING message...")
        
        success = webhook.send_rankings(
            top_players,
            title,
            description,
            color
        )
        
        if success:
            logger.info("✅ Successfully sent highlighted message to Discord!")
            logger.info("Check your Discord channel to see the GOLD highlighted final ranking!")
        else:
            logger.error("❌ Failed to send highlighted message")
            
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)

if __name__ == "__main__":
    test_highlighted_message()