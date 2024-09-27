from typing import Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

class ScheduleMeetingInput(BaseModel):
    meeting_title: str = Field(
        title="Meeting Title",
        description="The title of the meeting.",
        example="Weekly Team Meeting",
    )
    meeting_date: str = Field(
        title="Meeting Date",
        description="The date of the meeting.",
        example="2023-01-01",
    )
    meeting_time: str = Field(
        title="Meeting Time",
        description="The time of the meeting.",
        example="09:00 AM",
    )

class ScheduleMeetingTool(BaseTool):
    name = "schedule_meeting_tool"
    description = "Schedules a meeting based on user preferences."
    args_schema = ScheduleMeetingInput

    def _run(self, meeting_title, meeting_date, meeting_time) -> str:
        return f"Meeting Title: {meeting_title}\nMeeting Date: {meeting_date}\nMeeting Time: {meeting_time}"