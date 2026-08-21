from google import genai
from google.genai import types
from .models import DailyReportBatch
import config
import datetime

def generate_summary(git_data: list, antigravity_data: list) -> DailyReportBatch:
    """
    Calls Gemini API to generate a structured report from raw data.
    """
    if not config.GEMINI_API_KEY:
        # Fallback to empty if no key provided, usually for dry runs or when testing collectors
        print("Warning: GEMINI_API_KEY is not set. Skipping AI summarization.")
        return DailyReportBatch(items=[])
    
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    today = datetime.datetime.now().strftime("%d/%m/%Y")
    
    prompt = f"""
    You are an AI assistant that summarizes daily developer activities into a structured weekly report format.
    Today's date is: {today}.
    
    Analyze the following raw data collected from Git repositories and IDE artifacts, and synthesize it into a list of report items.
    Merge related commits/artifacts into a coherent summary per system.
    
    # Git Data:
    {git_data}
    
    # Antigravity IDE Artifacts Data:
    {antigravity_data}
    
    Ensure the date is set to {today}.
    Provide realistic Priority, Deadline, Status, Progress Percentage based on the context. If unknown, use reasonable defaults like '-' for deadline, 'In Progress', etc.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DailyReportBatch,
                temperature=0.2,
            ),
        )
        return DailyReportBatch.model_validate_json(response.text)
    except Exception as e:
        print(f"Failed to generate summary: {e}")
        return DailyReportBatch(items=[])
