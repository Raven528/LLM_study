import os
from openai import OpenAI

client_deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# Step 3: Define a function to call ChatGPT for completions with tools
def chat_completions(prompt_messages, tools=None, tool_choice="auto"):
    response = client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=prompt_messages,
        tools=tools,
        tool_choice=tool_choice,
    )
    return response.choices[0].message


# Step 1: Define the available functions in a dictionary
def get_weather(location, date):
    prompt = [
        {
            "role": "system",
            "content": "你是一个获取天气的助手，请随机杜撰一个天气查询结果",
        },
        {"role": "user", "content": f"请查询{location}在{date}时候的天气变化"},
    ]
    response = chat_completions(prompt)
    return response.content


def get_car_power(car):
    prompt = [
        {
            "role": "system",
            "content": "你是一个获取车辆电量的助手，请随机杜撰一个车辆电量情况",
        },
        {"role": "user", "content": f"请查询{car}的电量情况"},
    ]
    response = chat_completions(prompt)
    return response.content


def get_food(food):
    prompt = [
        {
            "role": "system",
            "content": "你是一个获取家里食物库存情况的助手，请随机杜撰一个食物库存情况",
        },
        {"role": "user", "content": f"请查询{food}情况"},
    ]
    response = chat_completions(prompt)
    return response.content


# Function map to easily look up function by name
available_functions = {
    "get_weather": get_weather,
    "get_car_power": get_car_power,
    "get_food": get_food,
}

# Step 2: Define the function schema (parameter definitions) in a separate structure
function_schemas = {
    "get_weather": {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                    },
                    "date": {
                        "type": "string",
                    },
                },
                "required": ["location", "date"],
            },
        },
    },
    "get_car_power": {
        "type": "function",
        "function": {
            "name": "get_car_power",
            "description": "查询车辆电量",
            "parameters": {
                "type": "object",
                "properties": {
                    "car": {
                        "type": "string",
                    }
                },
                "required": ["car"],
            },
        },
    },
    "get_food": {
        "type": "function",
        "function": {
            "name": "get_food",
            "description": "查询食物库存",
            "parameters": {
                "type": "object",
                "properties": {
                    "food": {
                        "type": "string",
                    }
                },
                "required": ["food"],
            },
        },
    },
}
