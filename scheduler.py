import schedule
import time
import subprocess
import os
import sys

def run_report():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running weekly report automator...")
    try:
        # Run the main.py script using the same python interpreter (the virtual environment)
        subprocess.run([sys.executable, "main.py"], check=True)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Report generation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error running report: {e}")
    except Exception as e:
         print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unexpected error: {e}")

if __name__ == "__main__":
    print("Starting Weekly Report Scheduler...")
    
    # --- Configuration Options ---
    # Run every Friday at 5:00 PM (17:00)
    schedule.every().friday.at("17:00").do(run_report)
    
    # Alternative: Run every day at 5:00 PM
    # schedule.every().day.at("17:00").do(run_report)
    
    # Alternative: Run every hour (for testing)
    # schedule.every(1).hours.do(run_report)
    
    print("Scheduler is active. Waiting for next scheduled run...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60) # Check every minute to conserve CPU
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
