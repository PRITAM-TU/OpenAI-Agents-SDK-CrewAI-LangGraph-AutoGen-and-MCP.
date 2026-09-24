import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI
from IPython.display import Markdown,display

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)



response = client.chat.completions.create(
    model="deepseek/deepseek-r1",
    messages=[
        {"role": "user", "content":"Tell me about the cat?"}
    ],
    max_completion_tokens=500,
    reasoning_effort="high",
    extra_headers={
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Game"
    }
)

ans=response.choices[0].message.content
print(ans)