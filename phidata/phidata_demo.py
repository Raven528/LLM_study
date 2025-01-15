from os import getenv
from phi.agent import Agent, RunResponse
from phi.model.openai.like import OpenAILike

# api = 'sk-a3aaa3ac792840e5b9755cf05c6afcb1'
agent = Agent(
    model=OpenAILike(
        id="qwen2.5-3b-instruct",
        api_key=getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
)

# Print the response in the terminal
agent.print_response("请介绍一下你自己吧")
