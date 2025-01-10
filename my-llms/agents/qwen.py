import os
from openai import OpenAI
import transformers

client = OpenAI(
    api_key="sk-k2bDg57DmI", # 如果您没有配置环境变量，请在此处用您的API Key进行替换
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
)

# # 图片调用Chat Completion API
# completion = client.chat.completions.create(
#     model="qwen-vl-plus-0809",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "这个图像是否存在ps等造假行为"
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                     "url": "https://ymm-nlp-sh.obs.cn-east-3.myhuaweicloud.com:443/fuhu.gu/CV/Avatar/%E5%A4%B4%E5%83%8F%E5%B9%BF%E5%91%8A.png?AccessKeyId=BBEWEU4YLEKY9Y3X2FAS&Expires=1742954008&Signature=UJ/FCsDI1q4uhwy2oSQ/YN%2Bu3Gg%3D"
#                     }
#                 }
#             ]
#         }
#         ]
#     )
# print(completion.model_dump_json())
# from pprint import pprint
# pprint(completion.choices[0].message.content)

completion = client.chat.completions.create(
    model="qwen-vl-ocr",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": "https://ymm-nlp-sh.obs.cn-east-3.myhuaweicloud.com:443/fuhu.gu/CV/hll_huoyuan/IMG_0462.PNG.JPG?AccessKeyId=BBEWEU4YLEKY9Y3X2FAS&Expires=1767425197&Signature=3jpBhEcT%2BTIOV5mee4Q1lCbkRy4%3D",
                    "min_pixels": 28 * 28 * 4,
                    "max_pixels": 28 * 28 * 1280
                },
                # 为保证识别效果，目前模型内部会统一使用"Read all the text in the image."进行识别，用户输入的文本不会生效。
                {"type": "text", "text": "Read all the text in the image."},
            ]
        }
    ])

print(completion.choices[0].message.content)
