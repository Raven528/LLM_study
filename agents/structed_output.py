from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
)

class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

completion = client.beta.chat.completions.parse(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
        {"role": "user", "content": "网页新闻贴吧知道网盘图片视频地图文库资讯采购百科京公网安备11000002000001号"}
    ],
    response_format=ResearchPaperExtraction,
)

research_paper = completion.choices[0].message.parsed
print(research_paper)
