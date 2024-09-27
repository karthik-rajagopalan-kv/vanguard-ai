from typing import Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

class CreateEmailInput(BaseModel):
    subject: str = Field(
        title="Subject",
        description="The subject of the email.",
        example="Meeting Follow-Up",
    )
    recipient: str = Field(
        title="Recipient",
        description="The recipient of the email.",
        example="John Doe",
    )
    message: str = Field(
        title="Message",
        description="The content of the email.",
        example="Hi John, I wanted to follow up on our meeting last week...",
    )

class CreateEmailTool(BaseTool):
    name = "create_email_tool"
    description = "Creates content for email."
    args_schema = CreateEmailInput

    def _run(self, subject, recipient, message) -> str:
        return f"Subject: {subject}\nRecipient: {recipient}\nMessage: {message}"