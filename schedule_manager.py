"""
Schedule Manager module for determining post types and timing.

This module handles scheduling logic for daily posts and weekly analysis.
"""

from datetime import datetime, timedelta
from typing import Dict, Any
import calendar
import logging

logger = logging.getLogger(__name__)


class ScheduleManager:
    """Manages scheduling logic for different types of posts."""

    @staticmethod
    def is_last_day_of_month(date: datetime = None) -> bool:
        """
        Check if the given date (or today) is the last day of the month.

        Args:
            date: Date to check (defaults to today)

        Returns:
            bool: True if it's the last day of the month
        """
        if date is None:
            date = datetime.now()

        # Get the last day of the current month
        last_day = calendar.monthrange(date.year, date.month)[1]
        
        return date.day == last_day

    @staticmethod
    def is_sunday(date: datetime = None) -> bool:
        """
        Check if the given date (or today) is a Sunday.

        Args:
            date: Date to check (defaults to today)

        Returns:
            bool: True if it's Sunday
        """
        if date is None:
            date = datetime.now()

        return date.weekday() == 6  # Sunday = 6

    @staticmethod
    def get_post_type(date: datetime = None) -> str:
        """
        Determine what type of post should be made today.

        Args:
            date: Date to check (defaults to today)

        Returns:
            str: Post type - 'monthly_final', 'weekly', 'daily', or 'weekly_and_daily'
        """
        if date is None:
            date = datetime.now()

        is_last_day = ScheduleManager.is_last_day_of_month(date)
        is_sunday_today = ScheduleManager.is_sunday(date)

        if is_last_day and is_sunday_today:
            return 'weekly_and_monthly_final'
        elif is_last_day:
            return 'monthly_final'
        elif is_sunday_today:
            return 'weekly_and_daily'
        else:
            return 'daily'

    @staticmethod
    def get_embed_config(post_type: str) -> Dict[str, Any]:
        """
        Get embed configuration based on post type.

        Args:
            post_type: Type of post

        Returns:
            dict: Configuration for the embed
        """
        configs = {
            'daily': {
                'title_suffix': '',
                'color': 3447003,  # Discord blue
                'highlight': False,
                'description_prefix': ''
            },
            'monthly_final': {
                'title_suffix': ' - 🏆 FINAL RANKING 🏆',
                'color': 16766720,  # Gold color
                'highlight': True,
                'description_prefix': '🎉 **FINAL MONTHLY RANKING** 🎉\n\n'
            },
            'weekly_and_daily': {
                'title_suffix': '',
                'color': 3447003,  # Discord blue
                'highlight': False,
                'description_prefix': ''
            },
            'weekly_and_monthly_final': {
                'title_suffix': ' - 🏆 FINAL RANKING 🏆',
                'color': 16766720,  # Gold color
                'highlight': True,
                'description_prefix': '🎉 **FINAL MONTHLY RANKING** 🎉\n\n'
            }
        }

        return configs.get(post_type, configs['daily'])

    @staticmethod
    def should_save_snapshot(date: datetime = None) -> bool:
        """
        Determine if a snapshot should be saved today.

        Args:
            date: Date to check (defaults to today)

        Returns:
            bool: True if snapshot should be saved (Sundays)
        """
        return ScheduleManager.is_sunday(date)

    @staticmethod
    def should_post_weekly_analysis(date: datetime = None) -> bool:
        """
        Determine if weekly analysis should be posted today.

        Args:
            date: Date to check (defaults to today)

        Returns:
            bool: True if weekly analysis should be posted (Sundays)
        """
        return ScheduleManager.is_sunday(date)

    @staticmethod
    def get_week_date_range() -> Dict[str, str]:
        """
        Get the date range for the current week (Monday to Sunday).

        Returns:
            dict: Dictionary with 'start' and 'end' date strings
        """
        today = datetime.now()
        
        # Calculate Monday of this week
        days_since_monday = today.weekday()
        monday = today - timedelta(days=days_since_monday)
        
        # Calculate Sunday of this week
        sunday = monday + timedelta(days=6)
        
        return {
            'start': monday.strftime('%d.%m.%Y'),
            'end': sunday.strftime('%d.%m.%Y')
        }

    @staticmethod
    def log_schedule_info(date: datetime = None):
        """
        Log current schedule information for debugging.

        Args:
            date: Date to check (defaults to today)
        """
        if date is None:
            date = datetime.now()

        post_type = ScheduleManager.get_post_type(date)
        is_last_day = ScheduleManager.is_last_day_of_month(date)
        is_sunday_today = ScheduleManager.is_sunday(date)
        should_snapshot = ScheduleManager.should_save_snapshot(date)
        should_weekly = ScheduleManager.should_post_weekly_analysis(date)

        logger.info(f"Schedule info for {date.strftime('%Y-%m-%d')}:")
        logger.info(f"  Post type: {post_type}")
        logger.info(f"  Last day of month: {is_last_day}")
        logger.info(f"  Is Sunday: {is_sunday_today}")
        logger.info(f"  Should save snapshot: {should_snapshot}")
        logger.info(f"  Should post weekly analysis: {should_weekly}")