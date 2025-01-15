from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools
from os import getenv
from phi.model.openai.like import OpenAILike

finance_agent = Agent(
    model=OpenAILike(
        id="qwen2.5-3b-instruct",
        api_key=getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)
finance_agent.print_response("Summarize analyst recommendations for NVDA", stream=True)
