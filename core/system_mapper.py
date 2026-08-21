import os

def map_system_name(repo_name_or_url: str) -> str:
    """
    Maps raw repository folder names to a more human-readable System Name.
    """
    mapping = {
        "olympia-frontend": "Olympia Portal",
        "admin-crm": "Admin CRM",
        "weekly-report-automator": "Weekly Report Automator"
    }
    
    if repo_name_or_url.endswith('.git'):
        repo_name_or_url = repo_name_or_url[:-4]
    
    base_name = os.path.basename(repo_name_or_url)
    
    if base_name in mapping:
        return mapping[base_name]
    
    return base_name.replace('-', ' ').replace('_', ' ').title()
