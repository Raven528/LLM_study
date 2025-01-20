import os
import json
from openai import OpenAI
from tools import function_schemas, available_functions

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


def main():
    # Step 4: Define the AI prompt that needs to be passed into the completion API
    ai_prompt = [
        {
            "role": "assistant",
            "content": "请逐步拆解user prompt中存在的任务,并对每一个任务调用合适的工具解决，最终给出结果",
        },
        {
            "role": "user",
            "content": "《新青年》这篇文章怎么样",
        },
    ]

    # Step 5: Extract functions dynamically based on the function_schemas
    ai_functions = [function_schemas[key] for key in available_functions.keys()]
    # Example of calling the chat function with the prompt and available functions
    first_response = chat_completions(ai_prompt, tools=ai_functions)
    print(first_response)
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
            print(f"{function_name}:\n function_response")
        print("汇总全部tools的输出为：")
        print(chat_completions(ai_prompt).content)


if __name__ == "__main__":
    main()
