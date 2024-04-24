"""
To make our agent conversational, we must also choose a prompt with a placeholder for our chat history.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Adapted from https://smith.langchain.com/hub/hwchase17/openai-tools-agent
prompt_assistant = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)