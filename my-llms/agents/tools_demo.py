import json
import openai
from utils import client_deepseek

# Step 1: Define the available functions in a dictionary
def search_baidu(keyword):
    return f"{keyword}是一个技术博主"

def search_google(keyword):
    return f"{keyword}很牛"

def search_bing(keyword):
    return f"{keyword}喜欢水鱼"

# Function map to easily look up function by name
available_functions = {
    "search_baidu": search_baidu,
    "search_google": search_google,
    "search_bing": search_bing
}

# Step 2: Define the function schema (parameter definitions) in a separate structure
function_schemas = {
    "search_baidu": {
        "type": "function",
        "function": {
            "name": "search_baidu",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    }
                },
                "required": ["keyword"],
            }
        }
    },
    "search_google": {
        "type": "function",
        "function": {
            "name": "search_google",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    }
                },
                "required": ["keyword"],
            }
        }
    },
    "search_bing": {
        "type": "function",
        "function": {
            "name": "search_bing",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                    }
                },
                "required": ["keyword"],
            }
        }
    }
}
# Step 3: Define a function to call ChatGPT for completions with tools
def chat_completions(prompt_messages, tools=None, tool_choice="auto"):
    response = client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=prompt_messages,
        tools = tools,
        tool_choice=tool_choice,
    )
    return response.choices[0].message
# Step 4: Define the AI prompt that needs to be passed into the completion API
ai_prompt = [
    {
        "role": "user",
        "content": f"汇总3个function的aiXpert的结果"
    }
]
# Step 5: Extract functions dynamically based on the function_schemas
ai_functions = [function_schemas[key] for key in available_functions.keys()]
# Example of calling the chat function with the prompt and available functions
first_response = chat_completions(ai_prompt, tools=ai_functions)
tool_calls = first_response.tool_calls
# 第一轮chat completions的结果加入prompt，再把function参数加入prompt，然后一起喂给chatgpt

if tool_calls:
    ai_prompt.append(first_response)
    # 将所有函数调用的结果拼接到消息列表里
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_response = function_to_call(**function_args)
        ai_prompt.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )
    print(chat_completions(ai_prompt))


