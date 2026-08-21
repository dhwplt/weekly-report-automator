import requests
import config

def send_telegram_alert(message: str):
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        return
        
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

def send_discord_alert(message: str):
    if not config.DISCORD_WEBHOOK_URL:
        return
        
    payload = {
        "content": message
    }
    try:
        requests.post(config.DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

def notify_success(date_str: str, project_count: int, project_names: list, commit_count: int):
    names_str = ", ".join(project_names)
    msg = (
        f"✅ <b>Weekly Report updated for {date_str}</b>:\n"
        f"Logged {project_count} projects ({names_str}) with {commit_count} commits/updates."
    )
    
    send_telegram_alert(msg)
    
    discord_msg = msg.replace("<b>", "**").replace("</b>", "**")
    send_discord_alert(discord_msg)
