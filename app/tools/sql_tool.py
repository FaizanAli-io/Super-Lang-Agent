import sqlite3
import requests
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase

from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv

load_dotenv()


def get_engine_for_chinook_db():
    """Pull sql file, populate in-memory database, and create engine."""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text

    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


llm = ChatOpenAI(model="gpt-4o-mini")
db = SQLDatabase(get_engine_for_chinook_db())
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)

agent_executor = create_react_agent(llm, toolkit.get_tools(), prompt=system_message)

user_input = "Which country's customers spent the most?"

for step in agent_executor.stream(
    {"messages": [HumanMessage(content=user_input)]},
    config={"configurable": {"thread_id": "abc123"}},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
