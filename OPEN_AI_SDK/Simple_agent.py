import os
import asyncio
from dotenv import find_dotenv, load_dotenv
#here we used Async openai caht 
from openai import AsyncOpenAI
import requests
import json   #and here we used the dumps the take all the data and convert the json foramte after taht we print them 
from agents import Agent, ModelSettings, function_tool,OpenAIChatCompletionsModel, Runner, set_tracing_disabled,SQLiteSession

load_dotenv(find_dotenv())

#here we have creeate the cliet with we call the llm 
client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# tahta is fro tracing for agent work floe 
set_tracing_disabled(True)

model = OpenAIChatCompletionsModel(
    model="deepseek/deepseek-chat",
    openai_client=client,# here we see new openai_client parament 
)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

session=SQLiteSession("12345","memeory.db")
#here we  create the tools tahta provide to the llm and after that we used it 
@function_tool
def push_tool(message: str) -> str:
    """ Send the given message to the user as a push notification """
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    result = requests.post(pushover_url, data=payload).status_code
    return f"Push sent with API status code {result}"

agent_1 = Agent(
    name="Summary agent",
    instructions="Summarize briefly using 3 bullet points.",
    model=model,
    model_settings=ModelSettings(max_tokens=300),
    tools=[push_tool]
)


async def main() -> None:
    print("Type 'exit' or 'quit' to stop the agent.")

    while True:
        try:
            prompt = input("Enter your query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if prompt.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        if not prompt:
            print("Please enter a question.")
            continue
        print("LLM")
        result = await Runner.run(agent_1, prompt, session=session)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())



