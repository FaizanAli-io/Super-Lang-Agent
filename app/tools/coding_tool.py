from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.riza.command import ExecPython

from langgraph.prebuilt import create_react_agent


tools = [ExecPython()]

model = ChatOpenAI(model="gpt-4o-mini")

agent_executor = create_react_agent(model, tools)

config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {
        "messages": [
            HumanMessage(
                content="`[4, -2, -2, 2, 1, -3, 1, 2, -2]` Given this list of integers, find the length and index of the longest contiguous subarray with a sum equal to zero."
            )
        ]
    },
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
