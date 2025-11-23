"""
Discord Webhook module for sending formatted messages.

This module creates Discord embeds and sends them via webhook.
"""

import requests
from typing import List, Dict, Any
from datetime import datetime


class DiscordWebhook:
    """Handler for sending messages to Discord via webhook."""

    def __init__(self, webhook_url: str):
        """
        Initialize the Discord webhook sender.

        Args:
            webhook_url: The Discord webhook URL
        """
        self.webhook_url = webhook_url

    def create_embed(
        self,
        title: str,
        description: str,
        color: int,
        players: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create a Discord embed with player rankings.

        Args:
            title: Embed title
            description: Embed description
            color: Embed color (decimal format)
            players: List of player dictionaries with rank, playername, and votes

        Returns:
            dict: Discord embed structure
        """
        # Build the fields for each player
        fields = []
        for player in players:
            rank = player.get('rank', '?')
            name = player.get('playername', 'Unknown')
            votes = player.get('votes', 0)

            # Create medal emoji for top 3
            rank_display = self._get_rank_display(rank)

            fields.append({
                "name": f"{rank_display} {name}",
                "value": f"**{votes}** votes",
                "inline": True
            })

        embed = {
            "title": title,
            "description": description,
            "color": color,
            "fields": fields,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "TopGames Top Voters"
            }
        }

        return embed

    @staticmethod
    def _get_rank_display(rank: int) -> str:
        """
        Get display string for rank with medals for top 3.

        Args:
            rank: Player rank

        Returns:
            str: Formatted rank string
        """
        medals = {
            1: "🥇",
            2: "🥈",
            3: "🥉"
        }
        if rank in medals:
            return medals[rank]
        return f"#{rank}"

    def send_embed(self, embed: Dict[str, Any]) -> bool:
        """
        Send embed to Discord via webhook.

        Args:
            embed: Discord embed structure

        Returns:
            bool: True if successful, False otherwise

        Raises:
            requests.RequestException: If the webhook request fails
        """
        payload = {
            "embeds": [embed]
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return True

        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to send Discord webhook: {str(e)}")

    def send_rankings(
        self,
        players: List[Dict[str, Any]],
        title: str,
        description: str,
        color: int
    ) -> bool:
        """
        Create and send player rankings to Discord.

        Args:
            players: List of player dictionaries
            title: Embed title
            description: Embed description
            color: Embed color

        Returns:
            bool: True if successful
        """
        if not players:
            # Send a message indicating no players
            embed = {
                "title": title,
                "description": "No voters to display at this time.",
                "color": color,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            embed = self.create_embed(title, description, color, players)

        return self.send_embed(embed)
