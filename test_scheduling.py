#!/usr/bin/env python3
"""
Test script to simulate different dates and see scheduling behavior.
"""

import sys
import logging
from datetime import datetime
from schedule_manager import ScheduleManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_dates():
    """Test different date scenarios."""
    test_dates = [
        datetime(2025, 11, 23),  # Today (Sunday)
        datetime(2025, 11, 24),  # Monday (regular day)
        datetime(2025, 11, 30),  # Saturday - Last day of November
        datetime(2025, 12, 1),   # Sunday - First day of December
        datetime(2025, 12, 31),  # Tuesday - Last day of December (New Year's Eve)
        datetime(2025, 1, 5),    # Sunday - Regular Sunday in January
    ]
    
    for test_date in test_dates:
        print(f"\n{'='*60}")
        print(f"Testing date: {test_date.strftime('%A, %Y-%m-%d')}")
        print(f"{'='*60}")
        
        post_type = ScheduleManager.get_post_type(test_date)
        embed_config = ScheduleManager.get_embed_config(post_type)
        is_last_day = ScheduleManager.is_last_day_of_month(test_date)
        is_sunday = ScheduleManager.is_sunday(test_date)
        should_snapshot = ScheduleManager.should_save_snapshot(test_date)
        should_weekly = ScheduleManager.should_post_weekly_analysis(test_date)
        
        print(f"Post type: {post_type}")
        print(f"Is last day of month: {is_last_day}")
        print(f"Is Sunday: {is_sunday}")
        print(f"Should save snapshot: {should_snapshot}")
        print(f"Should post weekly analysis: {should_weekly}")
        print(f"Title suffix: '{embed_config['title_suffix']}'")
        print(f"Embed color: {embed_config['color']} ({'Gold' if embed_config['color'] == 16766720 else 'Blue/Purple'})")
        print(f"Has highlight: {embed_config['highlight']}")

if __name__ == "__main__":
    test_dates()