from openai import AsyncOpenAI
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel
import os
from dotenv import find_dotenv, load_dotenv



load_dotenv(find_dotenv())


intro = """
You are a sales agent working for ComplAI, 
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI.
Write one cold sales email. Return only the email draft.
"""

instructions1 = intro + "Your email style is professional, serious, with gravitas and credibility."
instructions2 = intro + "Your email style is witty, engaging, and humorous."
instructions3 = intro + "Your email style is concise, to the point, in the style of a busy senior executive."

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

model = OpenAIChatCompletionsModel(
    model="openai/gpt-4o-mini",
    openai_client=client,
)

sales_agent1 = Agent(
    name="Professional Sales Agent",
    instructions=instructions1,
    model=model,
    model_settings=ModelSettings(max_tokens=200),
)
sales_agent2 = Agent(
    name="Humorous Sales Agent",
    instructions=instructions2,
    model=model,
    model_settings=ModelSettings(max_tokens=200),
)
sales_agent3 = Agent(
    name="Executive Sales Agent",
    instructions=instructions3,
    model=model,
    model_settings=ModelSettings(max_tokens=200),
)


description = "Use this tool to write a sales email. In the input, just instruct it to write a sales email."
tool1 = sales_agent1.as_tool(tool_name="sales_email_writer_1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_email_writer_2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_email_writer_3", tool_description=description)

tools = [tool1, tool2, tool3]





