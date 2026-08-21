# Weekly Report Automator

An enterprise-grade Python automation tool that scans multiple local Git repositories and Antigravity IDE workspace artifacts, summarizes daily activities using the Gemini API, and updates a stylized Weekly Report in both local Excel format and Google Sheets, with webhook alerts via Telegram and Discord.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

3. Fill out the `.env` variables:
   - `GEMINI_API_KEY`: Required to generate AI summaries.
   - `PARENT_PROJECTS_DIR`: Comma-separated list of paths containing your Git repositories (e.g. `C:\Projects, ~\Documents\GitHub`). Default is `~/Projects`.
   - `EXCEL_OUTPUT_PATH`: Path to save the `.xlsx` file.
   - `GOOGLE_SHEET_NAME`: The name of the Google Sheet (requires `service_account.json`).
   - `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: Optional, for Telegram alerts.
   - `DISCORD_WEBHOOK_URL`: Optional, for Discord alerts.

4. (Optional) Place `service_account.json` in the root directory if you want Google Sheets sync.

## Usage

Run the main script:
```bash
python main.py
```

Options:
- `--dry-run`: Run the summarization and display results in the console without exporting to Excel/Sheets or sending notifications.
- `--notify`: Force notifications even when running in `--dry-run` mode.

## Features
- **Git Repo Discovery**: Recursively finds `.git` repos up to 2 levels deep in the configured parent directories.
- **Antigravity Brain Collector**: Automatically scans IDE and CLI artifacts (`task.md`, `walkthrough.md`, `implementation_plan.md`) modified today.
- **AI Synthesis**: Generates a structured Weekly Report list combining all commits, changes, and task lists into clean output with priorities and statuses.
- **Styled Excel Export**: Creates dynamic tabs for the current week, applying enterprise-level styling, coloring, and auto-adjusting columns using `openpyxl`. Deduplicates in-place updates based on Date and System Name.
- **Google Sheets Sync**: Replicates the row data directly into a matching weekly tab on a Google Sheet.
- **Webhook Dispatch**: Alerts Telegram and/or Discord on a successful data generation pass.
