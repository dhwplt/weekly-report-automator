from pydantic import BaseModel, Field

class WeeklyReportItem(BaseModel):
    date: str = Field(description="Date in DD/MM/YYYY format")
    website_or_system: str = Field(
        description="Official name of the website or system"
    )
    task_scope: str = Field(
        description="Detailed bullet points of work done today"
    )
    priority: str = Field(
        description="Priority level: High, Medium, or Low"
    )
    deadline: str = Field(description="Target completion date or '-'")
    status: str = Field(
        description="Completed, In Progress, On Hold, or Pending Review"
    )
    progress_percentage: str = Field(
        description="Percentage formatted, e.g. 100%, 80%"
    )
    remarks: str = Field(
        description="Key commit hashes, blockers, test results, or next steps"
    )

class DailyReportBatch(BaseModel):
    items: list[WeeklyReportItem]
