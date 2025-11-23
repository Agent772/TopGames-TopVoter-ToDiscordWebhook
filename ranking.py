"""
Ranking module for validating and sorting player voting data.

This module processes raw API data and prepares it for display.
"""

from typing import List, Dict, Any


class RankingProcessor:
    """Processes and validates ranking data from API responses."""

    @staticmethod
    def validate_response(data: Dict[str, Any]) -> bool:
        """
        Validate that the API response has the expected structure.

        Args:
            data: The API response data

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(data, dict):
            return False

        if 'success' not in data or not data.get('success'):
            return False

        if 'players' not in data or not isinstance(data.get('players'), list):
            return False

        return True

    @staticmethod
    def validate_player(player: Dict[str, Any]) -> bool:
        """
        Validate that a player entry has required fields.

        Args:
            player: Player data dictionary

        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(player, dict):
            return False

        if 'playername' not in player or not player.get('playername'):
            return False

        if 'votes' not in player:
            return False

        try:
            int(player['votes'])
            return True
        except (ValueError, TypeError):
            return False

    def process_rankings(self, data: Dict[str, Any], max_count: int = 10) -> List[Dict[str, Any]]:
        """
        Process and sort player rankings.

        Args:
            data: Raw API response data
            max_count: Maximum number of players to return

        Returns:
            list: Sorted list of player dictionaries with rank added

        Raises:
            ValueError: If the data is invalid
        """
        if not self.validate_response(data):
            raise ValueError("Invalid API response structure")

        players = data.get('players', [])

        # Filter out invalid players
        valid_players = [p for p in players if self.validate_player(p)]

        if not valid_players:
            return []

        # Sort players by votes (descending)
        sorted_players = sorted(
            valid_players,
            key=lambda x: int(x['votes']),
            reverse=True
        )

        # Limit to max_count
        top_players = sorted_players[:max_count]

        # Add rank to each player
        for index, player in enumerate(top_players, start=1):
            player['rank'] = index

        return top_players


def get_top_rankings(data: Dict[str, Any], max_count: int = 10) -> List[Dict[str, Any]]:
    """
    Convenience function to get top rankings.

    Args:
        data: Raw API response data
        max_count: Maximum number of players to return

    Returns:
        list: Sorted list of top players with ranks
    """
    processor = RankingProcessor()
    return processor.process_rankings(data, max_count)
