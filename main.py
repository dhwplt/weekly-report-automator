import argparse
import datetime
from collectors.git_collector import collect_git_data
from collectors.antigravity_collector import collect_antigravity_data
from core.summarizer import generate_summary
from exporters.excel_exporter import export_to_excel
from exporters.sheet_exporter import export_to_google_sheets
from notifications.alerts import notify_success

def main():
    parser = argparse.ArgumentParser(description="Weekly Report Automator")
    parser.add_argument("--dry-run", action="store_true", help="Run without exporting or notifying")
    parser.add_argument("--notify", action="store_true", help="Force notifications even on dry run (for testing)")
    args = parser.parse_args()
    
    print("Gathering Git data...")
    git_data = collect_git_data()
    
    print("Gathering Antigravity artifacts data...")
    antigravity_data = collect_antigravity_data()
    
    if not git_data and not antigravity_data:
        print("No activities found for today. Exiting.")
        return
        
    print("Generating AI summary...")
    batch = generate_summary(git_data, antigravity_data)
    
    if args.dry_run:
        print("Dry run complete. Generated items:")
        for item in batch.items:
            print(f"- {item.website_or_system}: {item.status} ({item.progress_percentage})")
    else:
        export_to_excel(batch)
        export_to_google_sheets(batch)
        
    if not args.dry_run or args.notify:
        today_str = datetime.date.today().strftime("%d/%m/%Y")
        project_names = [item.website_or_system for item in batch.items]
        project_count = len(project_names)
        commit_count = sum(len(repo.get("commits", [])) for repo in git_data)
        
        if project_count > 0:
            notify_success(today_str, project_count, project_names, commit_count)

if __name__ == "__main__":
    main()
