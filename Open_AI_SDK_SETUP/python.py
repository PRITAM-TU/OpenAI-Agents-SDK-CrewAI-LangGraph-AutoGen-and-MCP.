import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)



response = client.chat.completions.create(
    model="deepseek/deepseek-v4.1-flash",
    messages=[
        {"role": "user", "content":"Build the profesonal protfolio with design and responsiveness alos and write production level code"}
    ],
    max_completion_tokens=50000,
    extra_headers={
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Game"
    }
)

print(response.choices[0].message.content)