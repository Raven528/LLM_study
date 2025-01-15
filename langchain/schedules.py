import os
import sqlite3
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import datetime

# 建表
# 连接到 SQLite 数据库
# 如果文件不存在，会自动在当前目录创建一个名为 'langchain.db' 的数据库文件
conn = sqlite3.connect('langchain.db')

# 创建一个 Cursor 对象并通过它执行 SQL 语句
c = conn.cursor()
# 创建表
c.execute('''
create table if not exists schedules 
(
    id          INTEGER
        primary key autoincrement,
    start_time  TEXT default (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) not null,
    description TEXT default ''                                                  not null
);
''')


# 提交事务
conn.commit()
# 关闭连接
conn.close()

print("数据库和表已成功创建！")



import sqlite3


def connect_db():
    """ 连接到数据库 """
    conn = sqlite3.connect('langchain.db')
    return conn
    
@tool
def add_schedule(start_time : str, description : str) -> str: 
    """ 新增日程，比如2024-05-03 20:00:00, 周会 """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO schedules (start_time, description) VALUES (?, ?);
    """, (start_time, description,))
    conn.commit()
    conn.close()
    return "true"

@tool
def delete_schedule_by_time(start_time : str) -> str:
    """ 根据时间删除日程 """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM schedules WHERE start_time = ?;
    """, (start_time,))
    conn.commit()
    conn.close()
    return "true"
    
@tool
def get_schedules_by_date(query_date : str) -> str:
    """ 根据日期查询日程，比如 获取2024-05-03的所有日程 """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT start_time, description FROM schedules WHERE start_time LIKE ?;
    """, (f"{query_date}%",))
    schedules = cursor.fetchall()
    conn.close()
    return str(schedules)

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
    openai_api_base="https://api.deepseek.com",
)
tools = [add_schedule, delete_schedule_by_time, get_schedules_by_date]
llm_with_tools = llm.bind_tools(tools)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个日程管理助手",
        ),
        ("placeholder", "{chat_history}"),
        ("user", "{input} \n\n 当前时间为：{current_time}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(llm_with_tools, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

def ask(question):
    res = agent_executor.invoke(
        {
            "input": question,
            "current_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    return res["output"]

while True:
    question = input(">")
    if question.lower() == '退出':
        break
    print(ask(question))

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

res = agent_with_chat_history.invoke(
        {
            "input": "我明天有啥日程？",
            "current_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        config={"configurable": {"session_id": "111"}}
    )
print(res)
print('======================')
print(store)















