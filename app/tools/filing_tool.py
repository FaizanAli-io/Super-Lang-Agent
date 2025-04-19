from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.agent_toolkits import FileManagementToolkit

from langgraph.prebuilt import create_react_agent

load_dotenv()

memory = MemorySaver()
model = ChatOpenAI(model="gpt-4o-mini")

tools = FileManagementToolkit(
    root_dir=r"C:\Users\Administrator\Desktop\AgentWithToolsBackend\tool-test",
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()

agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}
user_input = "Now list all files in the directory, read their content, and combine it into a single file."

for step in agent_executor.stream(
    {"messages": [HumanMessage(content=user_input)]},
    stream_mode="values",
    config=config,
):
    step["messages"][-1].pretty_print()
