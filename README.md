# Weekly Report Automator

An enterprise-grade Python automation tool that scans multiple local Git repositories and Antigravity IDE workspace artifacts, summarizes daily activities using the Gemini API, and updates a stylized Weekly Report in both local Excel format and Google Sheets, with webhook alerts via Telegram and Discord.

## 🚀 Team Installation & Setup

Follow these steps to install the tool on your machine:

**1. Clone the repository**
```bash
git clone https://github.com/dhwplt/weekly-report-automator.git
cd weekly-report-automator
```

**2. Install the package**
It is recommended to use a virtual environment, but you can install it directly. The `-e .` flag installs it so you can run the terminal commands globally from this folder.
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # On Windows PowerShell
pip install -e .
```

**3. Configure your Secrets (`.env`)**
Because API keys are blocked from GitHub, you need to create your own configuration:
```bash
cp .env.example .env
```
Open `.env` and fill out:
- `GEMINI_API_KEY`: Required to generate AI summaries.
- `PARENT_PROJECTS_DIR`: Comma-separated list of paths containing your Git repositories (e.g. `C:\Projects, ~\Documents\GitHub`). Default is `~/Projects`.
- `GOOGLE_SHEET_NAME`: The exact name of your target Google Sheet.

**4. Google Sheets Authentication (Personal Reporting)**
If you want to sync your reports to your own private Google Sheet:
1. Create a new Google Sheet (e.g., "My TaskLog") and put that exact name in your `.env` file under `GOOGLE_SHEET_NAME`.
2. Create a Service Account in your Google Cloud Console and generate a JSON key.
3. Rename the downloaded key to `service_account.json` and place it in the root of this directory.
4. Open your Google Sheet and click **Share**, then grant your new Service Account's email address **Editor** access.

---

## 💻 Usage

Because we packaged the tool using `pyproject.toml`, you don't need to type `python main.py`. You now have access to global terminal commands!

### Manual Run
To generate a report right now, simply run:
```bash
weekly-report
```
*Options:*
- `weekly-report --dry-run`: Run the summarization and display results in the console without exporting to Excel/Sheets or sending notifications.

### Automatic Scheduler (Terminal)
To run the tool automatically while leaving your terminal open, use:
```bash
weekly-report-scheduler
```

### Automatic Scheduler (Background / Windows)
If you don't want to leave a terminal open and want it to run silently in the background (even catching up if your laptop was asleep), run this command once in **PowerShell** (make sure you are in the project folder):
```powershell
$Action = New-ScheduledTaskAction -Execute '.\.venv\Scripts\python.exe' -Argument 'main.py' -WorkingDirectory (Get-Location).Path
$Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At 5:00PM
$Task = Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName "WeeklyReportAutomator" -Description "Automated Friday Weekly Report"
$Task.Settings.StartWhenAvailable = $true
Set-ScheduledTask -InputObject $Task
```

## Features
- **Git Repo Discovery**: Recursively finds `.git` repos up to 2 levels deep in the configured parent directories.
- **Antigravity Brain Collector**: Automatically scans IDE and CLI artifacts modified today.
- **AI Synthesis**: Generates a structured Weekly Report list combining all commits, changes, and task lists into clean output with priorities and statuses.
- **Styled Excel Export**: Creates dynamic tabs for the current week, applying enterprise-level styling, coloring, and auto-adjusting columns using `openpyxl`.
- **Google Sheets Sync**: Replicates the row data directly into a matching weekly tab on a Google Sheet.
- **Webhook Dispatch**: Alerts Telegram and/or Discord on a successful data generation pass.
