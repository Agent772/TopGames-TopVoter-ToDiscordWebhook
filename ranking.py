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

    def normalize_player_name(self, playername: str) -> str:
        """
        Normalize player name by removing ~ suffix and everything after it.
        
        Args:
            playername: Original player name
            
        Returns:
            str: Normalized player name without ~ suffix
        """
        if '~' in playername:
            return playername.split('~')[0]
        return playername

    def consolidate_players(self, players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Consolidate players with same normalized names by combining their votes.
        
        Args:
            players: List of player dictionaries
            
        Returns:
            list: List of consolidated players with combined votes
        """
        consolidated = {}
        
        for player in players:
            if not self.validate_player(player):
                continue
                
            original_name = player['playername']
            normalized_name = self.normalize_player_name(original_name)
            votes = int(player['votes'])
            
            if normalized_name in consolidated:
                # Add votes to existing normalized player
                consolidated[normalized_name]['votes'] += votes
                # Keep track of all original names for logging
                if consolidated[normalized_name]['original_names'] is None:
                    consolidated[normalized_name]['original_names'] = [consolidated[normalized_name]['playername']]
                consolidated[normalized_name]['original_names'].append(original_name)
            else:
                # Create new entry with normalized name
                consolidated[normalized_name] = {
                    'playername': normalized_name,
                    'votes': votes,
                    'original_names': [original_name] if original_name != normalized_name else []
                }
        
        # Convert back to list format
        consolidated_list = []
        for normalized_name, player_data in consolidated.items():
            consolidated_list.append({
                'playername': player_data['playername'],
                'votes': player_data['votes']
            })
            
            # Log consolidation if multiple names were merged
            if player_data.get('original_names') and len(player_data['original_names']) > 1:
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"Consolidated '{normalized_name}': {player_data['original_names']} -> {player_data['votes']} total votes")
        
        return consolidated_list

    def process_rankings(self, data: Dict[str, Any], max_count: int = 10) -> List[Dict[str, Any]]:
        """
        Process and sort player rankings with name normalization and vote consolidation.

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

        # Filter out invalid players first
        valid_players = [p for p in players if self.validate_player(p)]

        if not valid_players:
            return []

        # Consolidate players with similar names (remove ~ suffixes)
        consolidated_players = self.consolidate_players(valid_players)

        # Sort players by votes (descending)
        sorted_players = sorted(
            consolidated_players,
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
