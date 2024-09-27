from typing import Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool


class MeetingInsightInput(BaseModel):
    type: str = Field(
        title="Type",
        description="The type of insight to be generated.",
        example="summary",
        default="summary",
    )


class MeetingInsightTool(BaseTool):
    name = "meeting_insight_tool"
    description = (
        "Provides insights from past meetings. Gives an overall idea of the points to be discussed in the next meeting"
    )
    args_schema = MeetingInsightInput

    def _run(self, type) -> str:
        return "Insight"
