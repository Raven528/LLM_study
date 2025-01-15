import os
import re
import json
from openai import OpenAI

client_qwen = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

client_deepseek = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)


def llm_call_qwen(prompt, system_prompt = 'You are a helpful assistant.'):
    response = client_qwen.chat.completions.create(
        model="qwen-plus-1220",   # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}],
        ) 
    return response.choices[0].message.content

def llm_call_deepseek(prompt, system_prompt = 'You are a helpful assistant.',tools=None, tool_choice="auto"):
    response = client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}],
        tools = tools,
        tool_choice=tool_choice,
    )
    return response.choices[0].message.content

def llm_call_deepseek_message(prompt, system_prompt = 'You are a helpful assistant.',tools=None, tool_choice="auto"):
    response = client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}],
        tools = tools,
        tool_choice=tool_choice,
    )
    return response.choices[0].message

def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses 

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""

if __name__ == "__main__":
    print(llm_call_deepseek('你好,请介绍一下你自己'))
