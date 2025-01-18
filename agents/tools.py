import os
from openai import OpenAI
from pydantic import BaseModel, Field
from openai import pydantic_function_tool

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


class get_weather_scheme(BaseModel):
    location: str = (Field(description="地址信息，如南京"),)
    date: str = Field(description="日期信息，如20240101")


def get_car_power(car):
    prompt = [
        {
            "role": "system",
            "content": f"你是一个获取车辆电量的助手，请随机杜撰一辆车的电量情况",
        },
        {"role": "user", "content": f"请查询{car}的电量情况"},
    ]
    response = chat_completions(prompt)
    return response.content


class get_car_power_scheme(BaseModel):
    car: str = Field(description="具体的一辆车")


def get_food(food):
    prompt = [
        {
            "role": "system",
            "content": f"你是一个获取家里食物库存情况的助手，请随机杜撰食物的库存情况",
        },
        {"role": "user", "content": f"请查询{food}情况"},
    ]
    response = chat_completions(prompt)
    return response.content


class get_food_scheme(BaseModel):
    food: str = Field(description="一种食物")


# Function map to easily look up function by name
available_functions = {
    "get_weather": get_weather,
    "get_car_power": get_car_power,
    "get_food": get_food,
}

# Step 2: Define the function schema (parameter definitions) in a separate structure
function_schemas = {
    "get_weather": pydantic_function_tool(get_weather_scheme),
    "get_car_power": pydantic_function_tool(get_car_power_scheme),
    "get_food": pydantic_function_tool(get_food_scheme),
}
# "get_weather": {
#     "type": "function",
#     "function": {
#         "name": "get_weather",
#         "description": "查询天气",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                 },
#                 "date": {
#                     "type": "string",
#                 },
#             },
#             "required": ["location", "date"],
#         },
#     },
# },
# "get_car_power": {
#     "type": "function",
#     "function": {
#         "name": "get_car_power",
#         "description": "查询车辆电量",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "car": {
#                     "type": "string",
#                 }
#             },
#             "required": ["car"],
#         },
#     },
# },
# "get_food": {
#     "type": "function",
#     "function": {
#         "name": "get_food",
#         "description": "查询食物库存",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "food": {
#                     "type": "string",
#                 }
#             },
#             "required": ["food"],
#         },
#     },
# },
# }

if __name__ == "__main__":
    print(pydantic_function_tool(get_weather_scheme))
