"""
API Client module for fetching data from TopGames API.

This module handles HTTP requests to the TopGames API and returns player voting data.
"""

import requests
from typing import Dict, Any


class APIClient:
    """Client for interacting with the TopGames API."""

    def __init__(self, api_url: str, timeout: int = 10):
        """
        Initialize the API client.

        Args:
            api_url: The URL of the TopGames API endpoint
            timeout: Request timeout in seconds (default: 10)
        """
        self.api_url = api_url
        self.timeout = timeout

    def fetch_voters(self) -> Dict[str, Any]:
        """
        Fetch voter data from the API.

        Returns:
            dict: JSON response from the API containing voter data

        Raises:
            requests.RequestException: If the API request fails
            ValueError: If the response is not valid JSON
        """
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for bad status codes

            data = response.json()
            return data

        except requests.Timeout:
            raise requests.RequestException(f"Request to {self.api_url} timed out after {self.timeout} seconds")
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch data from API: {str(e)}")
        except ValueError as e:
            raise ValueError(f"Invalid JSON response from API: {str(e)}")


def fetch_top_voters(api_url: str) -> Dict[str, Any]:
    """
    Convenience function to fetch top voters.

    Args:
        api_url: The URL of the TopGames API endpoint

    Returns:
        dict: JSON response from the API containing voter data
    """
    client = APIClient(api_url)
    return client.fetch_voters()
