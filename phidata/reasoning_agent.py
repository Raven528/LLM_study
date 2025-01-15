from phi.agent import Agent
from os import getenv
from phi.model.openai.like import OpenAILike

task = (
    "Three missionaries and three cannibals need to cross a river. "
    "They have a boat that can carry up to two people at a time. "
    "If, at any time, the cannibals outnumber the missionaries on either side of the river, the cannibals will eat the missionaries. "
    "How can all six people get across the river safely? Provide a step-by-step solution and show the solutions as an ascii diagram"
)

reasoning_agent = Agent(
    model=OpenAILike(
        id="qwen2.5-3b-instruct",
        api_key=getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    reasoning=True, 
    markdown=True, 
    structured_outputs=True
)
reasoning_agent.print_response(task, stream=True, show_full_reasoning=True)
