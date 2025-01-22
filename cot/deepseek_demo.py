import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# Round 1
messages = [{"role": "user", "content": "9.11和9.8, 哪个更大?"}]
response = client.chat.completions.create(model="deepseek-reasoner", messages=messages)
reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content
