# TopGames TopVoter Discord Webhook

A comprehensive Python application that fetches top voter rankings from the TopGames API and posts them to Discord via webhook. Features advanced scheduling, weekly analysis, name consolidation, and automated month-end highlights.

## ✨ Features

### 📊 **Core Functionality**
- 🔄 Fetches player voting data from TopGames API
- ✅ Validates and sorts ranking data with smart name consolidation
- 🎨 Creates beautiful Discord embeds with medal emojis
- 🤖 Automated Discord webhook integration
- 📝 Comprehensive logging and error handling

### 🗓️ **Advanced Scheduling**
- ⏰ **Daily Posts**: Regular rankings at 23:55 (customizable)
- 📅 **Weekly Analysis**: Sunday posts with voting activity insights
- 🏆 **Month-End Highlights**: Gold-highlighted final rankings
- 💾 **Snapshot System**: Automatic weekly vote tracking

### 🎮 **Smart Player Management**
- 🔗 **Name Consolidation**: Automatically merges votes from multiple devices
- 📱 **Multi-Device Support**: Handles `Player~1`, `Player~mobile`, etc.
- 🎯 **Accurate Rankings**: No split votes for same player across devices

### 🎨 **Visual Enhancements**
- 🏅 Medal emojis (🥇🥈🥉) for monthly top 3
- 🔥 Special emojis (🔥⚡🌟) for weekly top performers  
- 🌍 German month names in titles
- 🎨 Color-coded embeds: Blue (daily), Purple (weekly), Gold (month-end)
- 📋 Clean 2-column layout for easy reading

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

## 🎮 Smart Name Consolidation

The bot automatically handles players voting from multiple devices by consolidating names with `~` suffixes:

### How It Works
When players vote from different devices, TopGames API may return separate entries like:
```json
{
  "players": [
    {"playername": "Player1", "votes": 15},
    {"playername": "Player1~mobile", "votes": 8},
    {"playername": "Player1~tablet", "votes": 5},
    {"playername": "Betty", "votes": 20},
    {"playername": "Betty~phone", "votes": 12}
  ]
}
```

### Automatic Consolidation
The bot **automatically combines** these into single entries:
```
Player1: 28 votes (15 + 8 + 5)
Betty: 32 votes (20 + 12)
```

### Supported Naming Patterns
- `PlayerName~1`, `PlayerName~2`, etc.
- `PlayerName~mobile`, `PlayerName~phone`
- `PlayerName~anything` → All become `PlayerName`

### Logging
Consolidations are logged for transparency:
```
INFO - Consolidated 'Player1': ['Player1~mobile', 'Player1~tablet'] -> 28 total votes
```

## 🚀 Usage

### 🧪 Testing & Manual Runs

**Test name consolidation:**
```bash
python test_consolidation.py
```

**Test scheduling behavior:**
```bash
python test_scheduling.py
```

**Test month-end highlighting:**
```bash
python test_highlight.py
```

**Run manually (current date logic):**
```bash
python main.py
```

### ⏰ Automated Scheduling

The bot is designed to run **daily at 23:55** and automatically determines what type of post to make:

#### 📅 **Post Schedule**
| Day Type | Posts | Features |
|----------|--------|----------|
| **Regular Days** | Daily ranking | 🔵 Blue embed, standard title |
| **Sundays** | Daily + Weekly analysis | 🔵 Daily + 🟣 Weekly insights |
| **Month-End** | Final ranking | 🟡 **Gold highlight** + 🏆 **FINAL RANKING** |
| **Last Sunday** | Final + Weekly | 🟡 Gold final + 🟣 Weekly analysis |

#### 🖥️ **Windows Task Scheduler Setup (Recommended)**

1. **Open Task Scheduler** (`taskschd.msc`)
2. **Create Basic Task**
3. **Configure:**
   - **Name:** `TopGames TopVoter Bot`
   - **Trigger:** Daily at `23:55`
   - **Action:** Start a program
   - **Program:** `D:\Git\TopGames-TopVoter-ToDiscordWebhook\.venv\Scripts\python.exe`
   - **Arguments:** `main.py`
   - **Start in:** `D:\Git\TopGames-TopVoter-ToDiscordWebhook\`

#### ⚡ **PowerShell Setup Command**
```powershell
# Run as Administrator
$action = New-ScheduledTaskAction -Execute "D:\Git\TopGames-TopVoter-ToDiscordWebhook\.venv\Scripts\python.exe" -Argument "main.py" -WorkingDirectory "D:\Git\TopGames-TopVoter-ToDiscordWebhook"
$trigger = New-ScheduledTaskTrigger -Daily -At "23:55"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "TopGames TopVoter Bot" -Action $action -Trigger $trigger -Settings $settings -Description "Daily TopGames voter rankings with weekly analysis"
```

#### 🐧 **Linux/Unix Cron Setup**
```bash
# Edit crontab
crontab -e

# Add daily job at 23:55
55 23 * * * cd /path/to/TopGames-TopVoter-ToDiscordWebhook && python3 main.py >> /var/log/topvoters.log 2>&1
```

## 📁 Project Structure

```
TopGames-TopVoter-ToDiscordWebhook/
├── 🚀 Core Files
│   ├── main.py                 # Main orchestrator with scheduling logic
│   ├── config.py               # Configuration management
│   ├── api_client.py           # TopGames API integration
│   ├── ranking.py              # Smart ranking with name consolidation
│   └── webhook.py              # Discord webhook with multi-format embeds
├── 🧠 Advanced Features
│   ├── schedule_manager.py     # Intelligent post scheduling
│   ├── snapshot_manager.py     # Weekly vote tracking system
│   └── snapshots/              # Weekly voting data storage
├── 🧪 Testing & Tools
│   ├── test_consolidation.py   # Test name merging functionality
│   ├── test_scheduling.py      # Test different date scenarios
│   ├── test_highlight.py       # Test month-end highlighting
│   └── cron_setup.txt         # Automation setup instructions
├── ⚙️ Configuration
│   ├── .env                    # Your environment variables
│   ├── .env.example           # Configuration template
│   ├── requirements.txt       # Python dependencies
│   └── cron.example           # Cron job examples
├── 📚 Documentation
│   ├── README.md              # This comprehensive guide
│   ├── ENHANCED_FEATURES.md   # Feature summary
│   └── LICENSE               # Project license
└── 🔧 Development
    ├── .gitignore             # Git ignore rules
    └── __pycache__/           # Python cache files
```

## 📊 API Response Format & Processing

### Expected TopGames API Response
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
      "votes": 25,
      "playername": "Player~mobile"
    },
    {
      "votes": 15, 
      "playername": "Player~tablet"
    },
    {
      "votes": 34,
      "playername": "Betty"
    }
  ]
}
```

### After Smart Processing
The bot automatically consolidates and processes this into:
```json
[
  {
    "rank": 1,
    "playername": "Borsti1", 
    "votes": 47
  },
  {
    "rank": 2,
    "playername": "Player",
    "votes": 40
  },
  {
    "rank": 3,
    "playername": "Betty",
    "votes": 34
  }
]
```

### Processing Features
- ✅ **Name Consolidation**: `Player~mobile` + `Player~tablet` → `Player`
- ✅ **Vote Aggregation**: Combines votes from all device variants
- ✅ **Data Validation**: Filters invalid entries
- ✅ **Smart Sorting**: Ranks by consolidated vote totals
- ✅ **Logging**: Transparent consolidation reporting

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

## ⚙️ Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_URL` | ✅ Yes | - | TopGames API endpoint URL |
| `DISCORD_WEBHOOK_URL` | ✅ Yes | - | Discord webhook URL |
| `EMBED_COLOR` | No | `3447003` | Default embed color (blue) |
| `EMBED_TITLE` | No | `"Top Voters"` | Base embed title (month added automatically) |
| `EMBED_DESCRIPTION` | No | `"Here are the top voters!"` | Embed description text |
| `MAX_VOTERS` | No | `10` | Maximum number of voters to display |

### 🎨 Color Codes
- **3447003** - Discord Blue (default/daily)
- **7506394** - Purple (weekly analysis) 
- **16766720** - Gold (month-end finals)

### 📝 Example Configuration
```env
API_URL=https://api.top-games.net/v1/servers/YOUR_SERVER_ID/players-ranking
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
EMBED_TITLE=Top Voters
EMBED_DESCRIPTION=Hier das Update der Top Voter dieses Monats!
MAX_VOTERS=15
EMBED_COLOR=3447003
```

## 🔧 Troubleshooting

### ⚠️ Configuration Issues
**"Configuration error: API_URL is not set"**
- ✅ Create `.env` file from `.env.example`
- ✅ Fill in all required environment variables
- ✅ Check for typos in variable names

**"Invalid JSON response from API"**
- ✅ Verify your `API_URL` is correct and accessible
- ✅ Check TopGames server status
- ✅ Test API in browser: should return valid JSON

### 🌐 Network Issues  
**"Failed to fetch data from API"**
- ✅ Check internet connection
- ✅ Verify firewall/antivirus isn't blocking requests
- ✅ Test API endpoint manually

**"Failed to send Discord webhook"**
- ✅ Verify webhook URL is correct and active
- ✅ Check Discord server permissions
- ✅ Ensure webhook wasn't deleted from Discord

### 🤖 Automation Issues
**Windows Task Scheduler not running**
- ✅ Check Task Scheduler service is running
- ✅ Verify task is enabled and scheduled
- ✅ Check task history for error details
- ✅ Ensure Python virtual environment path is correct

**Snapshots not saving**
- ✅ Check write permissions in bot directory
- ✅ Verify `snapshots/` directory exists
- ✅ Check disk space availability

### 📊 Data Issues
**Name consolidation not working**
- ✅ Check logs for consolidation messages
- ✅ Verify player names contain `~` character
- ✅ Run `test_consolidation.py` to verify functionality

**Weekly analysis shows no data**
- ✅ Ensure previous Sunday's snapshot exists
- ✅ Check if it's the first week (no baseline data)
- ✅ Verify snapshot files aren't corrupted

### 🔍 Debugging Commands
```bash
# Test name consolidation
python test_consolidation.py

# Test scheduling logic
python test_scheduling.py

# Test month-end highlighting
python test_highlight.py

# Manual run with full logging
python main.py
```

## 🛠️ Development & Customization

### 🏗️ Architecture Overview

The bot uses a **modular, extensible architecture**:

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **`main.py`** | Orchestration & workflow | Scheduling logic, error handling |
| **`config.py`** | Environment management | Validation, defaults, type conversion |
| **`api_client.py`** | TopGames API integration | HTTP requests, timeout handling |
| **`ranking.py`** | Data processing | **Name consolidation**, sorting, validation |
| **`webhook.py`** | Discord integration | **Multi-format embeds**, color coding |
| **`schedule_manager.py`** | **Smart scheduling** | Date logic, post type determination |
| **`snapshot_manager.py`** | **Weekly tracking** | Data persistence, diff calculations |

### 🎨 Customization Options

#### **Embed Appearance**
```python
# webhook.py - Modify embed colors
COLORS = {
    'daily': 3447003,      # Blue
    'weekly': 7506394,     # Purple  
    'monthly': 16766720    # Gold
}

# Customize emojis
DAILY_MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}
WEEKLY_MEDALS = {1: "🔥", 2: "⚡", 3: "🌟"}
```

#### **Scheduling Logic**
```python
# schedule_manager.py - Modify post timing
def custom_schedule():
    # Add custom logic for special events
    # Holiday schedules, tournament periods, etc.
```

#### **Name Processing**
```python  
# ranking.py - Extend consolidation rules
def custom_normalize_name(self, name):
    # Handle other naming patterns
    # Remove prefixes, normalize unicode, etc.
```

### 🔌 Extension Points

**Add new post types:**
1. Create new embed templates in `webhook.py`
2. Add logic to `schedule_manager.py`
3. Update main workflow in `main.py`

**Add data sources:**
1. Create new client in `api_client.py`
2. Add processing logic in `ranking.py`
3. Configure in `config.py`

**Add notifications:**
1. Extend webhook system for multiple channels
2. Add email, SMS, or other notification methods
3. Create conditional notification rules

## 🚀 Quick Start Summary

1. **📥 Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **⚙️ Configure Environment:**
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Add your API_URL and DISCORD_WEBHOOK_URL
   ```

3. **🧪 Test Everything:**
   ```bash
   python test_consolidation.py  # Test name merging
   python test_scheduling.py     # Test date logic  
   python test_highlight.py      # Test month-end highlighting
   python main.py               # Full test run
   ```

4. **⏰ Setup Automation:**
   - Use Windows Task Scheduler for daily 23:55 execution
   - Or setup cron job on Linux/Unix systems

5. **📊 Monitor Results:**
   - Check Discord channel for posts
   - Review logs for consolidation activities
   - Monitor `snapshots/` directory for weekly data

## 🎯 What You Get

✅ **Daily Rankings** with intelligent name consolidation  
✅ **Weekly Analysis** showing most active voters  
✅ **Month-End Highlights** with gold special formatting  
✅ **Multi-Device Support** via automatic name merging  
✅ **German Localization** with month names  
✅ **Professional Logging** and error handling  
✅ **Automated Snapshots** and data cleanup  

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional language localizations
- More embed formatting options  
- Integration with other gaming platforms
- Advanced analytics and statistics

## 💬 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Documentation**: Check `ENHANCED_FEATURES.md` for detailed feature info
- **Testing**: Use provided test scripts to verify functionality

---

**🎮 Built for TopGames Communities | 🤖 Powered by Discord Webhooks | 🐍 Made with Python**
