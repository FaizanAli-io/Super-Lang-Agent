from dotenv import load_dotenv

load_dotenv()

# import os
# from pprint import pprint

# from langchain_openai import OpenAI
# from langchain.agents import AgentType, initialize_agent


# llm = OpenAI(temperature=0)
# search = GoogleSerperAPIWrapper()

# tools = [
#     Tool(
#         name="Intermediate Answer",
#         func=search.run,
#         description="useful for when you need to ask with search",
#     )
# ]

# self_ask_with_search = initialize_agent(
#     tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True
# )

# res = self_ask_with_search.run(
#     "What is the hometown of the reigning men's U.S. Open champion?"
# )

# print(res)


# from langchain_core.tools import Tool
# from langchain_openai import ChatOpenAI
# from langchain_apify import ApifyActorsTool
# from langchain_core.messages import ToolMessage
# from langgraph.prebuilt import create_react_agent

# # from langchain_community.utilities import GoogleSerperAPIWrapper

# from langchain_community.tools import GoogleSerperResults

# model = ChatOpenAI(model="gpt-4o")


# tools = [
#     # ApifyActorsTool("apify/rag-web-browser"),
#     Tool(
#         name="Intermediate Answer",
#         func=GoogleSerperAPIWrapper().run,
#         description="useful for when you need to ask with search",
#     ),
# ]

# graph = create_react_agent(model, tools=tools)

# inputs = {"messages": [("user", "search for what is Apify")]}

# for s in graph.stream(inputs, stream_mode="values"):
#     message = s["messages"][-1]

#     if isinstance(message, ToolMessage):
#         continue

#     message.pretty_print()

# Import relevant functionality
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.tools import GoogleSerperResults
from langchain_apify import ApifyActorsTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langgraph.prebuilt import create_react_agent

# Create the agent
memory = MemorySaver()
model = ChatOpenAI(model="gpt-4o-mini")

search = GoogleSerperResults(max_results=1)
scrape = ApifyActorsTool("apify/rag-web-browser")
research = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [
    # search,
    # scrape,
    # research,
]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="Give me the plot summary of The Matrix")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
