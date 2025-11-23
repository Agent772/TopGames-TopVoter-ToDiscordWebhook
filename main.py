#!/usr/bin/env python3
"""
Main entry point for TopGames TopVoter Discord Webhook.

This script fetches top voters from TopGames API and posts them to Discord.
Supports daily rankings, weekly analysis, and month-end highlights.
"""

import sys
import logging
from datetime import datetime
from config import get_config
from api_client import fetch_top_voters
from ranking import get_top_rankings
from webhook import DiscordWebhook
from schedule_manager import ScheduleManager
from snapshot_manager import SnapshotManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to orchestrate the workflow."""
    try:
        logger.info("=" * 50)
        logger.info("Starting TopGames TopVoter Bot")
        logger.info("=" * 50)

        # Load and validate configuration
        logger.info("Loading configuration...")
        config = get_config()
        logger.info("Configuration loaded successfully")

        # Initialize managers
        snapshot_manager = SnapshotManager()
        
        # Log current schedule information
        ScheduleManager.log_schedule_info()
        
        # Determine what type of post to make
        post_type = ScheduleManager.get_post_type()
        embed_config = ScheduleManager.get_embed_config(post_type)
        
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

        # Save snapshot if it's Sunday
        if ScheduleManager.should_save_snapshot():
            logger.info("Saving weekly snapshot...")
            if snapshot_manager.save_snapshot(top_players):
                logger.info("Snapshot saved successfully")
                # Cleanup old snapshots
                snapshot_manager.cleanup_old_snapshots()
            else:
                logger.warning("Failed to save snapshot")

        # Initialize webhook
        webhook = DiscordWebhook(config.webhook_url)
        success_count = 0
        
        # Send daily/monthly ranking
        logger.info(f"Sending {post_type} rankings to Discord...")
        
        # Prepare title and description
        title = config.embed_title + embed_config['title_suffix']
        description = embed_config['description_prefix'] + config.embed_description
        color = embed_config.get('color', config.embed_color)
        
        success = webhook.send_rankings(
            top_players,
            title,
            description,
            color
        )

        if success:
            logger.info("Successfully sent rankings to Discord!")
            success_count += 1
        else:
            logger.error("Failed to send rankings to Discord")

        # Send weekly analysis if it's Sunday
        if ScheduleManager.should_post_weekly_analysis():
            logger.info("Calculating and sending weekly analysis...")
            
            # Calculate weekly votes
            weekly_players = snapshot_manager.calculate_weekly_votes(top_players)
            
            if weekly_players:
                logger.info(f"Found {len(weekly_players)} active weekly voters")
                # Log top weekly voters
                for player in weekly_players[:3]:
                    logger.info(
                        f"  Weekly #{player['rank']}. {player['playername']}: "
                        f"+{player['weekly_votes']} votes this week"
                    )
                
                # Get week date range
                week_range_dict = ScheduleManager.get_week_date_range()
                week_range = f"{week_range_dict['start']} - {week_range_dict['end']}"
                
                # Send weekly analysis
                weekly_success = webhook.send_weekly_analysis(weekly_players, week_range)
                
                if weekly_success:
                    logger.info("Successfully sent weekly analysis to Discord!")
                    success_count += 1
                else:
                    logger.error("Failed to send weekly analysis to Discord")
            else:
                logger.info("No weekly voting activity found, skipping weekly analysis")

        # Determine overall success
        expected_posts = 1  # Always expect daily post
        if ScheduleManager.should_post_weekly_analysis():
            expected_posts += 1  # Add weekly post if Sunday

        if success_count == expected_posts:
            logger.info(f"All posts sent successfully! ({success_count}/{expected_posts})")
            return 0
        else:
            logger.error(f"Some posts failed! ({success_count}/{expected_posts})")
            return 1

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1
    finally:
        logger.info("TopGames TopVoter Bot finished")
        logger.info("=" * 50)


if __name__ == "__main__":
    sys.exit(main())
