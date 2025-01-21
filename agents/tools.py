import os
from openai import OpenAI
from pydantic import BaseModel, Field
from openai import pydantic_function_tool

client_deepseek = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# Step 3: Define a function to call ChatGPT for completions with tools
def chat_completions(prompt_messages, tools=None):
    response = client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=prompt_messages,
        tools=tools,
    )
    return response.choices[0].message


class get_weather_scheme(BaseModel):
    location: str = (Field(description="地址信息，如南京"),)
    date: str = Field(description="日期信息，如20240101")


# Step 1: Define the available functions in a dictionary
def get_weather(location, date):
    prompt = [
        {
            "role": "system",
            "content": "你是一个获取天气的助手，请随机杜撰一个天气查询结果",
        },
        {
            "role": "user",
            "content": f"请查询{location}在{date}时候的天气变化",
        },
    ]
    response = chat_completions(prompt)
    return response.content


class get_car_power_scheme(BaseModel):
    car: str = Field(description="具体的一辆车")


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


class get_food_scheme(BaseModel):
    food: str = Field(description="一种食物")


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


class get_article_outline_scheme(BaseModel):
    article: str = Field(description="文章的主题、或者文正主体内容")


def get_article_outline(article):
    prompt = [
        {
            "role": "system",
            "content": """
                你是一位文本大纲生成专家，擅长根据用户的需求创建一个有条理且易于扩展成完整文章的大纲，你拥有强大的主题分析能力，能准确提取关键信息和核心要点。具备丰富的文案写作知识储备，熟悉各种文体和题材的文案大纲构建方法。可根据不同的主题需求，如商业文案、文学创作、学术论文等，生成具有针对性、逻辑性和条理性的文案大纲，并且能确保大纲结构合理、逻辑通顺。该大纲应该包含以下部分：
                引言：介绍主题背景，阐述撰写目的，并吸引读者兴趣。
                主体部分：第一段落：详细说明第一个关键点或论据，支持观点并引用相关数据或案例。
                第二段落：深入探讨第二个重点，继续论证或展开叙述，保持内容的连贯性和深度。
                第三段落：如果有必要，进一步讨论其他重要方面，或者提供不同的视角和证据。
                结论：总结所有要点，重申主要观点，并给出有力的结尾陈述，可以是呼吁行动、提出展望或其他形式的收尾。
                创意性标题：为文章构思一个引人注目的标题，确保它既反映了文章的核心内容又能激发读者的好奇心。""",
        },
        {"role": "user", "content": f"请生成{article}这篇文章的大纲"},
    ]
    response = chat_completions(prompt)
    return response.content


class get_prompt_scheme(BaseModel):
    content: str = Field(description="用户需求的描述")


def get_prompt(content):
    prompt = [
        {
            "role": "system",
            "content": """
                你是一位大模型提示词生成专家，请根据用户的需求编写一个智能助手的提示词，来指导大模型进行内容生成，要求：
                1. 以 Markdown 格式输出
                2. 贴合用户需求，描述智能助手的定位、能力、知识储备
                3. 提示词应清晰、精确、易于理解，在保持质量的同时，尽可能简洁
                4. 只输出提示词，不要输出多余解释""",
        },
        {"role": "user", "content": f"请生成能够满足以下需求的提示词:\n {content}"},
    ]
    response = chat_completions(prompt)
    return response.content


# Function map to easily look up function by name
available_functions = {
    "get_weather": get_weather,
    "get_car_power": get_car_power,
    "get_food": get_food,
    "get_article_outline": get_article_outline,
    "get_prompt": get_prompt,
}

# Step 2: Define the function schema (parameter definitions) in a separate structure
function_schemas = {
    "get_weather": pydantic_function_tool(model=get_weather_scheme, name="get_weather"),
    "get_car_power": pydantic_function_tool(
        model=get_car_power_scheme, name="get_car_power"
    ),
    "get_food": pydantic_function_tool(model=get_food_scheme, name="get_food"),
    "get_article_outline": pydantic_function_tool(
        model=get_article_outline_scheme, name="get_article_outline"
    ),
}

if __name__ == "__main__":
    import pdb

    pdb.set_trace()
    # print(pydantic_function_tool(get_weather_scheme, name="demo"))
    print(
        get_prompt("""
    User会提供一个对话文本给你，对话人为S:货主、D:司机，请逐步完成下面内容：
    1. 由于存在识别问题以及大量的口语化内容，文本会有许多同音字、同义字、重复等问题，尝试进行对话恢复，并总结对话中的有关费用的讨论；
    1. 根据对话中关于费用的讨论内容，判断讨论的费用类型、对应费用金额，以及两人是否认可此费用；
    2. 将费用划分且仅划分为五类[高速费,搬运费,停车费,等候费,运费,其他费用]，这五类的定义为：
        高速费：D走高速、过桥等需要支付的费用
        搬运费：D在装/卸货地搬运货物而支付的费用
        停车费：D在装/卸货地停车产生的费用
        等候费：D在装/卸货地等待/排队时间超过平台免费等候时间产生的费用
        运费：D运输货物需要的费用
        其他费用：所有不属于上述费用类型的费用,
    3. 请将结果按照json格式输出，具体要求为：
        对每种费用类型，只能返回上述六类费用类型
        对每种费用类型，提及费用字段类型为bool，若对话中讨论了此字段，则为'True'，否则为'False'
        对每种费用类型，费用金额字段类型为int，需要提供精确数值而非范围，若未提及具体金额，则返回-1
        对每种费用类型，达成一致字段类型为bool，当且仅当双方提及某类费用类型且互相认同（注意，不一定提及金额）时为'True'  
        下面是一个输出示例：
            { 
            '高速费': {'提及费用': False, '费用金额': -1, '达成一致': False},
            '搬运费': {'提及费用': True,'费用金额': -1, '达成一致': True},
            '停车费': {'提及费用': True,'费用金额': 10, '达成一致': False},
            '等候费': {'提及费用': False,'费用金额': -1, '达成一致': False},
            '运费': {'提及费用': True,'费用金额': 1000, '达成一致': True},
            '其他费用': {'提及费用': False,'费用金额': -1, '达成一致': False}}
    4. 请仅输出json结果，不要输出其他内容
    """)
    )
