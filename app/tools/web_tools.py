from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.tools import GoogleSerperResults
from langchain_apify import ApifyActorsTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langgraph.prebuilt import create_react_agent

memory = MemorySaver()
model = ChatOpenAI(model="gpt-4o-mini")

search = GoogleSerperResults(max_results=1)
scrape = ApifyActorsTool("apify/rag-web-browser")
research = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [
    search,
    scrape,
    research,
]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [HumanMessage(content="")]},
    config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
