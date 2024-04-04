import os
from typing import Callable
# from dotenv import load_dotenv, find_dotenv

from langchain_openai import ChatOpenAI
# from langchain.tools import GooglePlacesTool
from langchain_community.tools import GooglePlacesTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from . import prompts


def shoppingAgent(model:str = "gpt-3.5-turbo-1106", prompt = prompts.prompt_assistant, verbose: bool = False) -> Callable:
    """
    This function returns a function that takes a message and returns a response.

    Required:
    make sure to set the OPENAI_API_KEY and GPLACES_API_KEY variable before running this function.
    """

    # _ = load_dotenv(find_dotenv()) # read local .env file

    os.environ['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
    os.environ["GPLACES_API_KEY"] = os.environ["GMAP_API_KEY"]

    chat = ChatOpenAI(model=model)
    places_tool = GooglePlacesTool()
    tools = [places_tool]

    agent = create_openai_tools_agent(chat, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=verbose)

    chat_history_for_chain = ChatMessageHistory()

    conversational_agent_executor = RunnableWithMessageHistory(
        agent_executor,
        # TBD: define `get_by_session_id` function
        lambda session_id: chat_history_for_chain,
        input_messages_key="input",
        output_messages_key="output",
        history_messages_key="chat_history",
    )

    return conversational_agent_executor
