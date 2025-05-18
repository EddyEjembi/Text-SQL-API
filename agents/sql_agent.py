from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from llm.chat import ChatLLM
from utils.prompt_template import SQL_PROMPT_TEMPLATE


def sql_agent(db, question: str, model: str, provider: str, api_key: str):
    """
    Create a SQL agent using the provided database and system message.
    """
    # Initialize the LLM
    llm = ChatLLM(model=model, provider=provider, api_key=api_key).llm()

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    tools = toolkit.get_tools()

    agent_executor = create_react_agent(llm, tools, prompt=SQL_PROMPT_TEMPLATE)

    message = {"messages": [{"role": "user", "content": question}]}
    
    # Run the agent
    _response = agent_executor.invoke(message)
    # Print the final message
    response = _response["messages"][-1]
    final_response = response.content

    if final_response is None:
        final_response = "No response from the agent. Please try again."

    # Print the final response
    print("\n--- Final AI Response ---")
    print(_response)

    return final_response