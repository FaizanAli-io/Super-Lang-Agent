import sqlite3
import requests

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI
from langchain_apify import ApifyActorsTool
from langchain_google_community import GmailToolkit
from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools import GoogleSerperResults
from langchain_community.tools.riza.command import ExecPython
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from dotenv import load_dotenv

load_dotenv()


class ToolManager:
    def __init__(self):
        self.tools = {}
        self.memory = MemorySaver()
        self.model = ChatOpenAI(model="gpt-4o-mini")

        self.tool_map = {
            "WEB_SEARCH": self._load_search,
            "WEB_SCRAPING": self._load_scrape,
            "WEB_BROWSING": self._load_browse,
            "RESEARCH": self._load_research,
            "FILE_READER": self._load_file,
            "DATABASE_ACCESS": self._load_sql,
            "EMAIL_ASSISTANT": self._load_gmail,
            "CODE_INTERPRETER": self._load_execpython,
        }

    def load_tools(self, tool_names: list[str]):
        for name in tool_names:
            func = self.tool_map.get(name)
            if not func:
                raise NotImplementedError(f'Tool "{name}" is not implemented.')
            self.tools[name] = func()

    def _load_search(self):
        return [GoogleSerperResults(max_results=1)]

    def _load_scrape(self):
        return [ApifyActorsTool("apify/web-scraper")]

    def _load_browse(self):
        return [ApifyActorsTool("apify/rag-web-browser")]

    def _load_research(self):
        return [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())]

    def _load_file(self):
        return FileManagementToolkit(
            root_dir=r"C:\Users\Administrator\Desktop\AgentWithToolsBackend\tool-test",
            selected_tools=["read_file", "write_file", "list_directory"],
        ).get_tools()

    def _load_gmail(self):
        return GmailToolkit().get_tools()

    def _load_execpython(self):
        return [ExecPython()]

    def _load_sql(self):
        url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
        sql_script = requests.get(url).text
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.executescript(sql_script)
        engine = create_engine(
            "sqlite://",
            creator=lambda: conn,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
        db = SQLDatabase(engine)
        return SQLDatabaseToolkit(db=db, llm=self.model).get_tools()

    def create_executor(self):
        all_tools = [t for sublist in self.tools.values() for t in sublist]
        return create_react_agent(self.model, all_tools, checkpointer=self.memory)
