"""
Snapshot Manager module for tracking weekly voting data.

This module handles saving snapshots and calculating weekly vote differences.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SnapshotManager:
    """Manages vote snapshots and weekly analysis."""

    def __init__(self, snapshots_dir: str = "snapshots"):
        """
        Initialize the snapshot manager.

        Args:
            snapshots_dir: Directory to store snapshot files
        """
        self.snapshots_dir = snapshots_dir
        self._ensure_snapshots_dir()

    def _ensure_snapshots_dir(self):
        """Create snapshots directory if it doesn't exist."""
        if not os.path.exists(self.snapshots_dir):
            os.makedirs(self.snapshots_dir)
            logger.info(f"Created snapshots directory: {self.snapshots_dir}")

    def get_snapshot_filename(self, date: datetime) -> str:
        """
        Get snapshot filename for a given date.

        Args:
            date: Date for the snapshot

        Returns:
            str: Filename for the snapshot
        """
        return f"snapshot_{date.strftime('%Y%m%d')}.json"

    def save_snapshot(self, players_data: List[Dict[str, Any]], date: Optional[datetime] = None) -> bool:
        """
        Save a snapshot of current voting data.

        Args:
            players_data: Current players voting data
            date: Date for the snapshot (defaults to today)

        Returns:
            bool: True if successful, False otherwise
        """
        if date is None:
            date = datetime.now()

        try:
            # Create a clean snapshot data structure
            snapshot = {
                "date": date.isoformat(),
                "timestamp": datetime.now().isoformat(),
                "players": {}
            }

            # Store player data with votes
            for player in players_data:
                if 'playername' in player and 'votes' in player:
                    snapshot["players"][player['playername']] = int(player['votes'])

            filename = self.get_snapshot_filename(date)
            filepath = os.path.join(self.snapshots_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)

            logger.info(f"Snapshot saved: {filename} with {len(snapshot['players'])} players")
            return True

        except Exception as e:
            logger.error(f"Failed to save snapshot: {e}")
            return False

    def load_snapshot(self, date: datetime) -> Optional[Dict[str, Any]]:
        """
        Load a snapshot from a specific date.

        Args:
            date: Date of the snapshot to load

        Returns:
            dict or None: Snapshot data if found, None otherwise
        """
        try:
            filename = self.get_snapshot_filename(date)
            filepath = os.path.join(self.snapshots_dir, filename)

            if not os.path.exists(filepath):
                logger.info(f"Snapshot not found: {filename}")
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                snapshot = json.load(f)

            logger.info(f"Snapshot loaded: {filename}")
            return snapshot

        except Exception as e:
            logger.error(f"Failed to load snapshot {filename}: {e}")
            return None

    def calculate_weekly_votes(self, current_players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate weekly vote differences by comparing with last Sunday's snapshot.

        Args:
            current_players: Current player voting data

        Returns:
            list: Players with weekly vote counts, sorted by weekly votes
        """
        try:
            # Find last Sunday
            today = datetime.now()
            days_since_sunday = today.weekday() + 1  # Monday = 0, Sunday = 6
            if days_since_sunday == 7:  # Today is Sunday
                days_since_sunday = 7  # Use last Sunday instead of today
            
            last_sunday = today - timedelta(days=days_since_sunday)
            
            logger.info(f"Calculating weekly votes since: {last_sunday.strftime('%Y-%m-%d')}")

            # Load last Sunday's snapshot
            last_snapshot = self.load_snapshot(last_sunday)
            if not last_snapshot:
                logger.warning("No snapshot found for last Sunday, cannot calculate weekly votes")
                return []

            # Calculate differences
            weekly_players = []
            current_votes = {p['playername']: int(p['votes']) for p in current_players if 'playername' in p and 'votes' in p}

            for playername, current_count in current_votes.items():
                last_count = last_snapshot['players'].get(playername, 0)
                weekly_votes = current_count - last_count

                if weekly_votes > 0:  # Only include players who voted this week
                    weekly_players.append({
                        'playername': playername,
                        'weekly_votes': weekly_votes,
                        'total_votes': current_count,
                        'last_week_votes': last_count
                    })

            # Sort by weekly votes (descending)
            weekly_players.sort(key=lambda x: x['weekly_votes'], reverse=True)

            # Add ranks
            for i, player in enumerate(weekly_players, 1):
                player['rank'] = i

            logger.info(f"Calculated weekly votes for {len(weekly_players)} active players")
            return weekly_players

        except Exception as e:
            logger.error(f"Failed to calculate weekly votes: {e}")
            return []

    def cleanup_old_snapshots(self, keep_weeks: int = 12):
        """
        Remove snapshots older than specified weeks.

        Args:
            keep_weeks: Number of weeks to keep (default: 12)
        """
        try:
            cutoff_date = datetime.now() - timedelta(weeks=keep_weeks)
            
            for filename in os.listdir(self.snapshots_dir):
                if filename.startswith("snapshot_") and filename.endswith(".json"):
                    try:
                        # Extract date from filename
                        date_str = filename[9:17]  # snapshot_YYYYMMDD.json
                        file_date = datetime.strptime(date_str, '%Y%m%d')
                        
                        if file_date < cutoff_date:
                            filepath = os.path.join(self.snapshots_dir, filename)
                            os.remove(filepath)
                            logger.info(f"Removed old snapshot: {filename}")
                    except ValueError:
                        # Skip files with invalid date format
                        continue

        except Exception as e:
            logger.error(f"Failed to cleanup old snapshots: {e}")