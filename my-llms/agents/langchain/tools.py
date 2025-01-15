import sqlite3
from langchain_core.tools import tool

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

