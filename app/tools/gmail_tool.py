from dotenv import load_dotenv

load_dotenv()


from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_google_community import GmailToolkit

from langgraph.prebuilt import create_react_agent


toolkit = GmailToolkit()
tools = toolkit.get_tools()

model = ChatOpenAI(model="gpt-4o-mini")

agent_executor = create_react_agent(model, tools)

user_input = "Send 5 emails to Faizan Ali (fali.abdulali@gmail.com) explaining tool based agents in langchain and langgraph, in increasing order of complexity. The first email should be a simple explanation, the second should include an example, the third should include a code snippet, the fourth should include a diagram, and the fifth should include a video link. Make sure to use a friendly tone and keep it concise. Once finished, list the last 10 unread emails in the inbox."

for step in agent_executor.stream(
    {"messages": [HumanMessage(content=user_input)]},
    config={"configurable": {"thread_id": "abc123"}},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
