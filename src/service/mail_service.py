from langchain_openai import ChatOpenAI
from src.prompts.analyze_mail import prompt
from langchain_core.messages import SystemMessage, HumanMessage


class MailService:
    def __init__(self):
        pass

    def email_action(self, email_content: str):
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        user_prompt = f"Mail content: {email_content}"
        response = llm.invoke([SystemMessage(content=prompt), HumanMessage(content=user_prompt)])

        return response.content
