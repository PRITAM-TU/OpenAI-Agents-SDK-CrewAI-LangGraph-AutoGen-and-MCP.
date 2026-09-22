import os
from dotenv import load_dotenv,find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

prompt = input("Enter your prompt: ")

response = client.chat.completions.create(
    model="deepseek/deepseek-v4.1-flash",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_completion_tokens=10000,
    extra_headers={
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "Game"
    }
)

print(response.choices[0].message.content)