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
        # Build the fields for each player in 2-column layout
        fields = []
        
        # Create names column
        names_list = []
        votes_list = []
        
        for player in players:
            rank = player.get('rank', '?')
            name = player.get('playername', 'Unknown')
            votes = player.get('votes', 0)

            # Create medal emoji for top 3
            rank_display = self._get_rank_display(rank)
            
            names_list.append(f"{rank_display} {name}")
            votes_list.append(f"**{votes}** votes")

        # Add the two columns as fields
        if names_list:
            fields.append({
                "name": "Rank & Player",
                "value": "\n".join(names_list),
                "inline": True
            })
            fields.append({
                "name": "Votes",
                "value": "\n".join(votes_list),
                "inline": True
            })

        # Add current month in German to title
        german_months = {
            1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni",
            7: "Juli", 8: "August", 9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
        }
        current_month = german_months[datetime.now().month]
        title_with_month = f"{title}: {current_month}"

        embed = {
            "title": title_with_month,
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

    def send_weekly_analysis(
        self,
        weekly_players: List[Dict[str, Any]],
        week_range: str,
        color: int = 7506394  # Purple color for weekly posts
    ) -> bool:
        """
        Create and send weekly voting analysis to Discord.

        Args:
            weekly_players: List of players with weekly vote data
            week_range: Date range string (e.g., "17.11 - 23.11.2025")
            color: Embed color for weekly posts

        Returns:
            bool: True if successful
        """
        if not weekly_players:
            embed = {
                "title": "📊 Wöchentliche Voting-Analyse",
                "description": f"**Woche: {week_range}**\n\nKeine Aktivitäten in dieser Woche gefunden.",
                "color": color,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "TopGames Weekly Analysis"
                }
            }
        else:
            # Create weekly analysis embed
            names_list = []
            votes_list = []
            
            for player in weekly_players[:10]:  # Limit to top 10
                rank = player.get('rank', '?')
                name = player.get('playername', 'Unknown')
                weekly_votes = player.get('weekly_votes', 0)
                
                # Use different emojis for weekly rankings
                rank_display = self._get_weekly_rank_display(rank)
                names_list.append(f"{rank_display} {name}")
                votes_list.append(f"**+{weekly_votes}** Votes")

            fields = []
            if names_list:
                fields.append({
                    "name": "🏃‍♂️ Aktivste Voter",
                    "value": "\n".join(names_list),
                    "inline": True
                })
                fields.append({
                    "name": "📈 Wöchentliche Votes",
                    "value": "\n".join(votes_list),
                    "inline": True
                })

            embed = {
                "title": "📊 Wöchentliche Voting-Analyse",
                "description": f"**Woche: {week_range}**\n\nHier sind die aktivsten Voter dieser Woche!",
                "color": color,
                "fields": fields,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "TopGames Weekly Analysis"
                }
            }

        return self.send_embed(embed)

    @staticmethod
    def _get_weekly_rank_display(rank: int) -> str:
        """
        Get display string for weekly rankings with different emojis.

        Args:
            rank: Player rank

        Returns:
            str: Formatted rank string
        """
        weekly_medals = {
            1: "🔥",  # Fire for most active
            2: "⚡",  # Lightning for second
            3: "🌟"   # Star for third
        }
        if rank in weekly_medals:
            return weekly_medals[rank]
        return f"#{rank}"
