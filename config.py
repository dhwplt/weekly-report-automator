import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Keys and External Services
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Google Sheets Configuration
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Weekly Work Report")
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")

# Local Excel Configuration
EXCEL_OUTPUT_PATH = Path(os.getenv("EXCEL_OUTPUT_PATH", "./Weekly_Report.xlsx")).resolve()

# Directory Configuration
# Parse PARENT_PROJECTS_DIR as a comma-separated list, defaulting to ~/Projects
_projects_dirs_raw = os.getenv("PARENT_PROJECTS_DIR", str(Path.home() / "Projects"))
PARENT_PROJECTS_DIRS = [Path(p.strip()).expanduser().resolve() for p in _projects_dirs_raw.split(",") if p.strip()]

# Antigravity paths
ANTIGRAVITY_BRAIN_PATHS = [
    Path.home() / ".gemini" / "antigravity" / "brain",
    Path.home() / ".gemini" / "antigravity-cli" / "brain",
    Path.home() / ".gemini" / "antigravity-ide" / "brain",
]
