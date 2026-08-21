import os
import datetime
from pathlib import Path
import config
from core.system_mapper import map_system_name

def collect_antigravity_data() -> list[dict]:
    """
    Scans Antigravity brain directories for files modified today.
    """
    all_data = []
    today = datetime.date.today()
    
    target_files = ['task.md', 'walkthrough.md', 'implementation_plan.md']
    
    for brain_path in config.ANTIGRAVITY_BRAIN_PATHS:
        if not brain_path.exists():
            continue
            
        # brain directory contains conversation IDs which contain the target files
        for conv_dir in brain_path.iterdir():
            if not conv_dir.is_dir():
                continue
                
            conv_data = {
                "conversation_id": conv_dir.name,
                "system_name": map_system_name(conv_dir.name),
                "artifacts": []
            }
            
            has_today_updates = False
            for target in target_files:
                file_path = conv_dir / target
                if file_path.exists():
                    mtime = datetime.date.fromtimestamp(file_path.stat().st_mtime)
                    if mtime == today:
                        has_today_updates = True
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                # Summarize content to save tokens
                                conv_data["artifacts"].append({
                                    "filename": target,
                                    "content_preview": content[:1000] + ("..." if len(content) > 1000 else "")
                                })
                        except Exception:
                            pass
            
            if has_today_updates:
                all_data.append(conv_data)
                
    return all_data
