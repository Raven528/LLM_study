from openai import OpenAI
import pandas as pd
import json
import os

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def llm_call(prompt, system_prompt="You are a helpful assistant."):
    """Call the OpenAI LLM with a given prompt and system configuration."""
    completion = client.chat.completions.create(
        model="deepseek-chat",
        # model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    return completion.choices[0].message.content


# data_processing_steps = """
#     User会提供一个对话文本给你，对话人为S:货主、D:司机，请逐步完成下面内容：
#     1. 由于存在识别问题以及大量的口语化内容，文本会有许多同音字、同义字、重复等问题，尝试进行对话恢复，并总结对话中的有关费用的讨论；
#     1. 根据对话中关于费用的讨论内容，判断讨论的费用类型、对应费用金额，以及两人是否认可此费用；
#     2. 将费用划分且仅划分为五类[高速费,搬运费,停车费,等候费,运费,其他费用]，这五类的定义为：
#         高速费：D走高速、过桥等需要支付的费用
#         搬运费：D在装/卸货地搬运货物而支付的费用
#         停车费：D在装/卸货地停车产生的费用
#         等候费：D在装/卸货地等待/排队时间超过平台免费等候时间产生的费用
#         运费：D运输货物需要的费用
#         其他费用：所有不属于上述费用类型的费用,
#     3. 请将结果按照json格式输出，具体要求为：
#         对每种费用类型，只能返回上述六类费用类型
#         对每种费用类型，提及费用字段类型为bool，若对话中讨论了此字段，则为'True'，否则为'False'
#         对每种费用类型，费用金额字段类型为int，需要提供精确数值而非范围，若未提及具体金额，则返回-1
#         对每种费用类型，达成一致字段类型为bool，当且仅当双方提及某类费用类型且互相认同（注意，不一定提及金额）时为'True'
#         下面是一个输出示例：
#             {
#             '高速费': {'提及费用': False, '费用金额': -1, '达成一致': False},
#             '搬运费': {'提及费用': True,'费用金额': -1, '达成一致': True},
#             '停车费': {'提及费用': True,'费用金额': 10, '达成一致': False},
#             '等候费': {'提及费用': False,'费用金额': -1, '达成一致': False},
#             '运费': {'提及费用': True,'费用金额': 1000, '达成一致': True},
#             '其他费用': {'提及费用': False,'费用金额': -1, '达成一致': False}}
#     4. 请仅输出json结果，不要输出其他内容
#     """

get_extra_fee_prompt_llm = """
    请严格按照以下流程处理用户提供的货主与司机对话文本：

    一、处理流程
    1. 对话清洗与结构化
    - 修正同音字/错别字（如"微盟"→"物流"）
    - 合并重复/冗余语句（如"对对对"→"对"）
    - 消除口语化干扰词（如"呃"、"啊"）
    - 用[货主]/[司机]标记对话角色

    2. 费用信息分析
    - 定位所有涉及费用的对话片段
    - 识别费用相关要素：费用类型、金额、支付意向

    3. 费用分类与验证
    - 严格匹配六类费用定义（含新增说明）：
        ▫️ 高速费：需出现"高速/过路/过桥"等关键词
        ▫️ 搬运费：需涉及"搬运/装卸/人力"等场景
        ▫️ 停车费：需明确"停车/车位"等上下文
        ▫️ 等候费：需提及"等/排队/超时"等情形
        ▫️ 运费：必须与运输服务直接相关
        ▫️ 其他费用：不满足上述任一类型的费用
    - 金额提取规则：仅接受精确数值，模糊表述（如"加一点"）视为-1

    二、输出规范
    1. 必须生成完整六类费用结构，不可遗漏
    2. 达成一致判定标准（同时满足）：
    - 双方至少各提及一次该费用
    - 存在明确同意表述（如"好"/"行"/"可以"）
    3. JSON格式要求：
    {
        "高速费": {"提及费用": bool, "费用金额": int, "达成一致": bool},
        "搬运费": {"提及费用": bool, "费用金额": int, "达成一致": bool},
        "停车费": {"提及费用": bool, "费用金额": int, "达成一致": bool},
        "等候费": {"提及费用": bool, "费用金额": int, "达成一致": bool},
        "运费": {"提及费用": bool, "费用金额": int, "达成一致": bool},
        "其他费用": {"提及费用": bool, "费用金额": int, "达成一致": bool}
    }
    4.请将结果按照json格式输出，不要输出其他内容

    三、示例强化
    [对话] 司机："平台价不含高速费，加50行吗？" 货主："最多加50"
    [分析]
    - 明确提及"高速费"且金额50
    - 司机提出请求，货主明确同意金额
    - 其他费用类型无相关讨论
    [输出] 
    {
    "高速费": {"提及费用": True, "费用金额": 50, "达成一致": True},
    "搬运费": {"提及费用": False, "费用金额": -1, "达成一致": False},
    ...
    }
"""


def llm_parse(report):
    result = llm_call(report, get_extra_fee_prompt_llm)
    reslut_json = json.loads(result)
    return reslut_json


report = """
{"dialogue":[["D:喂。","S:喂。","D:喂喂，经理啊啊，我是送刚刚帮你送货去顺德那个司机啊。","S:嗯。","S:啊。","D:呃，哦，那个货已经已经送过去了，刚刚卸完我，呃，把那个单已经结束了，但是那个高速费我拍给你了，然后呃，你帮我找一下，去那个微信那里吧，我发了图片给你的在平台。","S:嗯。","S:没有啊，你你要加在平台上哦。","D:啊，我我我发了图片，我按的太快，那个结束那个单的嘛。","D:然后我把那个凭那个凭证也发给你了吗？发给你看着呢。","S:嗯，我要报销的呀，老板你要给我。","D:然后我把两，呃，把。","D:嗯。","D:他报价我有我我。","S:你现在加不了吗？","D:我也要凭证啊，我按的太快，没有按上去那个平台，呃，我在平台发的图片给你吧。","S:啊。","D:我没骗你的，你看你可以看看吧，我发图片给你的在平台。","S:哎呀，我不是说你骗我，我没有说你骗我，但是你要你你可以的话，你就帮我弄到平台上喽。","D:嗯。","D:嗯嗯。","D:要要要要要要。","S:因为这个的话，要不然我等一下很难报销的。","D:又又要打给客服的，又打给客服，要麻烦了，我又把那个车上。","S:对呀，你弄一下，加在平台上。","D:很难弄的，那我我也我也想啊，你明白吗？","S:知道了，嗯，知道了多少？","D:哎。","D:啊，好吧？麻烦你啊，21块钱，我我发个平台给你看吧，你你可以找一下就可以了啊，麻烦你啊，麻烦你啊。啊，不好意思啊。啊，好的好的啊。","S:不是。","S:哦，哦哦哦哦好好，好好好哎呀。"]]}
"""
result = llm_parse(report)
print(result)

# df = pd.read_csv('/data/fuhu.gu/workspace/NLP/extra_fee_communication/Datasets/extra_fee_20250113.csv')
# df.dropna(axis=1, how='all',inplace=True)
#
# results_json = df['录音文本'].apply(llm_parse).apply(pd.Series)
# fees = results_json.columns.tolist()
# df_demo = pd.concat([df, results_json], axis=1)
#
# def parse_fee(fee_detail):
#     is_talk = fee_detail.get('提及费用', False)
#     amount = fee_detail.get('费用金额', -1)
#     is_deal = fee_detail.get('达成一致', False)
#
#     fee_type = 2 if is_talk and is_deal else (1 if is_talk else 0)
#
#     price = amount if amount > -1 else None
#     return fee_type, price
#
# for each in fees:
#     print(f'===={each}====')
#     df_demo[[f'llm_{each}类型', f'llm_{each}价格']] = df_demo[each].apply(parse_fee).apply(pd.Series)
#
# df_demo.to_csv('demo.csv', index=False, encoding='utf-8-sig')
