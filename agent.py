import os
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents.format_scratchpad.tools import format_to_tool_messages
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers import ToolsAgentOutputParser

from tools.email_tool import CreateEmailTool
from tools.meeting_insights_tool import MeetingInsightTool
from tools.schedule_meeeting_tool import ScheduleMeetingTool

agent_prompt = (
    "You are an intelligent assistant with access to the following tools:\n"
    "1. schedule_meeting_tool: Use this tool to schedule, reschedule, or cancel meetings based on user preferences or availability.\n"
    "2. create_email_tool: Use this tool to help users write, edit, or optimize emails for professional communication.\n"
    "3. meeting_insight_tool: Use this tool to provide summaries, key points, or insights from past meetings.\n\n"
    "Please follow the instructions below to assist the user:\n"
    "\t- If the user wants to arrange or adjust meetings, use the Meeting Scheduling Tool."
    "Also keep in mind to generate a insight based on previous meetings using the meeting_insight_tool and join its response with response from schedule_meeting_tool"
    "\t- If the user needs help writing or refining an email, use the Email Crafting Tool."
    "\t- If the user requests insights or summaries from past meetings, use the Meeting Insights Tool."
    "\t- If the query does not align with any of the available tools, respond directly without invoking a tool."
    "\t- Invoke all tool only once. Do not invoke the same tool multiple times."
    "Your should always use the necessary tool, if required according to the user query. If no tool is required, respond accordingly."
)

tools = [MeetingInsightTool(), CreateEmailTool(), ScheduleMeetingTool()]

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", agent_prompt),
        MessagesPlaceholder("chat_history"),
        MessagesPlaceholder("agent_scratchpad"),
        HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=["input"], template="{input}")),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (
    RunnablePassthrough.assign(agent_scratchpad=lambda x: format_to_tool_messages(x["intermediate_steps"]))
    | qa_prompt
    | llm.bind_tools(tools)
    | ToolsAgentOutputParser()
)

agent_executor = AgentExecutor(
    agent=chain,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
    max_iterations=5,
)
