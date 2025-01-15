from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, SimpleJsonOutputParser
from langchain_core.runnables import RunnablePassthrough
import os

model = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
    openai_api_base="https://api.deepseek.com",
)

write_prompt = ChatPromptTemplate.from_template(
    "写一篇关于电影{topic}的观后感，用markdown格式，不少于800字。"
)

output_parser = StrOutputParser()
write_chain = write_prompt | model | output_parser

print(write_chain.invoke("十二怒汉"))

analysis_prompt = ChatPromptTemplate.from_template("给下面这篇文章评分 \n\n {content}")

composed_chain = {"content": write_chain} | analysis_prompt | model | StrOutputParser()

print(composed_chain.invoke("十二怒汉"))
