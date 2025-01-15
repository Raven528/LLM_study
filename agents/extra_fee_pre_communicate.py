from openai import OpenAI
import pandas as pd
import json
import os

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

def llm_call(prompt, system_prompt="You are a helpful assistant."):
    """Call the OpenAI LLM with a given prompt and system configuration."""
    completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        response_format={
            'type': 'json_object'
        }
    )
    return completion.choices[0].message.content

data_processing_steps = """
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
    """

def llm_parse(report):
    result = llm_call(report, data_processing_steps)
    reslut_json = json.loads(result)
    return reslut_json

report = """
{"dialogue":[["S:喂，哎哎。","D:嗯。","D:喂。","D:喂，老板，你好。","D:你那个到的那个开的那个是吧？","S:没错。","S:对对对对。","D:喂。","D:你你今天晚上能不能给我装上车啊？","S:就是你现在几点10:00谁帮你装货啊？","D:嗯。","S:都下班了，明天早上装可以。","D:嗯。","D:我是问你现在能能帮我装上车了，那就好一点咯。","S:没人呢，已经下班了。","D:我可以看到。","D:嗯。","D:你。","D:你你你就是。","D:那个条子凳子多重啊。","S:不中的。","D:那不是你你有一个人在那里我帮你装都可以呀。","S:怎么装啊？都锁门了那，游乐场里面。","S:我。","D:这样啊。","S:对啊。","S:对。","D:对。","D:那你明天装你这个价格能不能加一点嘛？明天装的话。","S:怎么加的？我天天都叫车，你拉的又不是你一辆车。","D:你这里过去这。","S:最近几天，最近几天都在这里叫车，都是这个价。","S:你接20块高速费给你。","D:这个估计八十公八十公里哦。","S:你接给给20块那个高速费你两百两百六两百八。","D:280。","S:又不是你装第一车的，在这最近几天都在那里装。","D:嗯。","S:啊。","S:嗯。","D:你你手机端就是给280是吧？","S:啊。","S:对啊。","D:290块钱买加个10块钱的30块钱高速费了，总共是78块钱的高速费。","S:啊。","S:什么七十八？","D:啊。","D:我过来是78块钱呢。","S:20块高速费的。","D:20块钱高速费。哦，我来我来是从消费过来嗯。","S:你这里阳江上，然后在北斗那边上20块的。","D:我。","D:哦，我。","D:我来是从新过来，因为你走走到太的话，八十多公里刚好一半。","S:不是开庭啊，是北斗那里去金鸡那里啊。","D:280。","S:才20块高速费你再走西部原来高速路那里。","D:喂。","D:280，你这个明天早上几点说话啊？","S:呃，8:00。","D:8:00了。","S:嗯。","D:嗯，那行吧行吧，我在这里等你明天早上。","D:现在没有单过去了。","S:你可以直接去我们去没有你直接去游乐场那边等了。","S:你需要洗澡，我安排人给你。","D:我知道我。","D:我我我过去没多远啦，我现在这里过去只有只有5公里啊。","S:嗯。","S:那你可以需要谁找的安排公园开门给你进去。","D:我我所以说我说你如果今天晚上能给我东西最好咯。","S:没人了，你自己又装不了的，又要拉那边拿那个三轮车的拉出来的。","S:那怎么装？","D:我装不了啊，我怎么装不了你？你有人我都说了，你有人在那里我都可以装啊。","S:传不了那我锁门了，公司那边都不开门了，你怎么怎么进呢？","D:啊，那你那里不开门就没办法了，你说我装不了，我我装我就装不了。","S:对呀。","S:没装不了的，您的门都进不了啊，都锁了下班了，你刚好9:00下班。","D:嗯。","S:嗯。","D:嗯，那行吧行吧那那那我我我我我我我等你吧。","S:那你接单了接单，我安排明天早上8:00，你直接去那个财务乐园啊，去那里我叫人在门口等你。","D:嗯。","D:嗯。","S:财务乐园，你知不知道？","D:嗯，好好好好。","D:嗯，可以可以。","S:你知不知道好好。","S:你别打我电话，我明天不听电话，我找到了。","S:嗯。","D:你你你你你你把那个电话你把那边装货的电话发到那个发到那个信息里面就可以了吧？","S:行行行，我发给你，你直接明天打这个电话给他。","D:啊，你你发的那个信息里面把装货人的电话发到信息里面就可以了嘛。","S:嗯，好。","D:嗯，好好好好。","S:啊。","D:嗯。","D:嗯，再见啊。","S:5:00。"]]}
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
