# TopGames TopVoter Discord Webhook

A Python application that fetches top voter rankings from the TopGames API and posts them to Discord via webhook. The application validates and sorts the ranking data, builds a formatted Discord embed, and sends it automatically via cron.

## Features

- 🔄 Fetches player voting data from TopGames API
- ✅ Validates and sorts ranking data
- 🎨 Creates beautiful Discord embeds with medal emojis for top 3
- 🤖 Sends rankings to Discord via webhook
- ⏰ Designed to run via cron for automated updates
- 🔧 Fully configurable via environment variables
- 📝 Comprehensive logging

## Requirements

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Agent772/TopGames-TopVoter-ToDiscordWebhook.git
   cd TopGames-TopVoter-ToDiscordWebhook
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your configuration:
   - `API_URL`: Your TopGames API endpoint URL
   - `DISCORD_WEBHOOK_URL`: Your Discord webhook URL (see [Creating a Webhook](#creating-a-discord-webhook))
   - `EMBED_COLOR`: (Optional) Discord embed color in decimal format
   - `EMBED_TITLE`: (Optional) Title for the embed
   - `EMBED_DESCRIPTION`: (Optional) Description for the embed
   - `MAX_VOTERS`: (Optional) Maximum number of voters to display

## Usage

### Running Manually

Run the script directly:
```bash
python3 main.py
```

Or make it executable and run:
```bash
chmod +x main.py
./main.py
```

### Running via Cron

To automatically post rankings at regular intervals, set up a cron job:

1. **Edit your crontab:**
   ```bash
   crontab -e
   ```

2. **Add a cron job entry:**

   **Example 1: Run every hour**
   ```cron
   0 * * * * cd /path/to/TopGames-TopVoter-ToDiscordWebhook && /usr/bin/python3 main.py >> /var/log/topvoters.log 2>&1
   ```

   **Example 2: Run every day at 9:00 AM**
   ```cron
   0 9 * * * cd /path/to/TopGames-TopVoter-ToDiscordWebhook && /usr/bin/python3 main.py >> /var/log/topvoters.log 2>&1
   ```

   **Example 3: Run every 6 hours**
   ```cron
   0 */6 * * * cd /path/to/TopGames-TopVoter-ToDiscordWebhook && /usr/bin/python3 main.py >> /var/log/topvoters.log 2>&1
   ```

   **Example 4: Run twice a day (8 AM and 8 PM)**
   ```cron
   0 8,20 * * * cd /path/to/TopGames-TopVoter-ToDiscordWebhook && /usr/bin/python3 main.py >> /var/log/topvoters.log 2>&1
   ```

   **Cron schedule format:**
   ```
   * * * * * command
   │ │ │ │ │
   │ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
   │ │ │ └───── Month (1-12)
   │ │ └─────── Day of month (1-31)
   │ └───────── Hour (0-23)
   └─────────── Minute (0-59)
   ```

3. **Verify the cron job:**
   ```bash
   crontab -l
   ```

4. **Check logs:**
   ```bash
   tail -f /var/log/topvoters.log
   ```

## Project Structure

```
TopGames-TopVoter-ToDiscordWebhook/
├── main.py              # Main entry point
├── config.py            # Configuration management
├── api_client.py        # API client for fetching data
├── ranking.py           # Ranking validation and sorting logic
├── webhook.py           # Discord webhook sender
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .env                 # Your actual environment variables (not committed)
├── .gitignore          # Git ignore rules
├── LICENSE             # Project license
└── README.md           # This file
```

## API Response Format

The application expects the TopGames API to return JSON in this format:

```json
{
  "code": 200,
  "success": true,
  "players": [
    {
      "votes": 47,
      "playername": "Borsti1"
    },
    {
      "votes": 34,
      "playername": "Betty"
    }
  ]
}
```

## Creating a Discord Webhook

1. Open your Discord server
2. Go to Server Settings → Integrations → Webhooks
3. Click "New Webhook" or "Create Webhook"
4. Configure the webhook:
   - Set a name (e.g., "Top Voters Bot")
   - Choose the channel where rankings should be posted
   - (Optional) Upload an avatar
5. Click "Copy Webhook URL"
6. Paste the URL into your `.env` file as `DISCORD_WEBHOOK_URL`

## Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_URL` | Yes | - | TopGames API endpoint URL |
| `DISCORD_WEBHOOK_URL` | Yes | - | Discord webhook URL |
| `EMBED_COLOR` | No | 3447003 | Embed color (decimal format) |
| `EMBED_TITLE` | No | "Top Voters" | Embed title |
| `EMBED_DESCRIPTION` | No | "Here are the top voters!" | Embed description |
| `MAX_VOTERS` | No | 10 | Maximum number of voters to display |

## Troubleshooting

### "Configuration error: API_URL is not set"
Make sure you've created a `.env` file from `.env.example` and filled in all required values.

### "Failed to fetch data from API"
- Check that your `API_URL` is correct
- Verify the API is accessible from your server
- Check your internet connection

### "Failed to send Discord webhook"
- Verify your `DISCORD_WEBHOOK_URL` is correct
- Make sure the webhook hasn't been deleted from Discord
- Check that the bot has permissions to post in the channel

### Cron job not running
- Verify cron service is running: `systemctl status cron`
- Check cron logs: `grep CRON /var/log/syslog`
- Use absolute paths in your cron command
- Make sure the script has execute permissions: `chmod +x main.py`

## Development

### Module Overview

- **config.py**: Manages environment variables and configuration validation
- **api_client.py**: Handles HTTP requests to the TopGames API
- **ranking.py**: Validates player data and sorts by vote count
- **webhook.py**: Creates Discord embeds and sends them via webhook
- **main.py**: Orchestrates the entire workflow

### Adding Features

The modular design makes it easy to extend:
- Add new data sources by creating additional API clients
- Customize embed formatting in `webhook.py`
- Add data transformation logic in `ranking.py`
- Extend configuration options in `config.py`

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
