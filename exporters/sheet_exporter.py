import os
import datetime
import gspread
from google.oauth2.service_account import Credentials
import config
from core.models import DailyReportBatch
from .excel_exporter import get_week_range_str

def export_to_google_sheets(batch: DailyReportBatch):
    if not batch.items:
        return
        
    try:
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        if not os.path.exists(config.GOOGLE_SERVICE_ACCOUNT_FILE):
            print(f"Warning: {config.GOOGLE_SERVICE_ACCOUNT_FILE} not found. Skipping Google Sheets sync.")
            return
            
        credentials = Credentials.from_service_account_file(
            config.GOOGLE_SERVICE_ACCOUNT_FILE,
            scopes=scopes
        )
        
        gc = gspread.authorize(credentials)
        sh = gc.open(config.GOOGLE_SHEET_NAME)
        
        week_str = get_week_range_str()
        
        try:
            worksheet = sh.worksheet(week_str)
        except gspread.exceptions.WorksheetNotFound:
            try:
                template_ws = sh.worksheet('Template')
                worksheet = sh.duplicate_sheet(template_ws.id, new_sheet_name=week_str)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sh.add_worksheet(title=week_str, rows=100, cols=20)
                headers = ["Date", "Website/System", "Task / Scope", "Priority", "Deadline", "Status", "Progress (%)", "Remarks"]
                worksheet.insert_row(headers, index=1)
                
        existing_data = worksheet.get_all_values()
        existing_entries = {}
        
        for i, row in enumerate(existing_data):
            if len(row) >= 2:
                date_val = row[0]
                sys_val = row[1]
                if date_val and sys_val:
                    existing_entries[(date_val, sys_val)] = i + 1
                    
        next_new_row = len(existing_data) + 1
        
        cells_to_update = []
        for item in batch.items:
            key = (item.date, item.website_or_system)
            if key in existing_entries:
                row_idx = existing_entries[key]
            else:
                row_idx = next_new_row
                next_new_row += 1
                
            row_data = [
                item.date,
                item.website_or_system,
                item.task_scope,
                item.priority,
                item.deadline,
                item.status,
                item.progress_percentage,
                item.remarks
            ]
            
            for col_idx, val in enumerate(row_data, 1):
                cells_to_update.append(gspread.Cell(row=row_idx, col=col_idx, value=val))
                
        if cells_to_update:
            worksheet.update_cells(cells_to_update)
            print(f"Google Sheets sync completed for {len(batch.items)} items on tab {week_str}")
            
    except Exception as e:
        print(f"Failed to export to Google Sheets: {e}")
