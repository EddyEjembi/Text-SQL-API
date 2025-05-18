"""
LangGraph Agent Tools that handle SQL generation and execution.
"""
from langchain_core.prompts import PromptTemplate
from typing import List
from utils.prompt_template import SQL_PROMPT_TEMPLATE
from llm.chat import chatLLM
import re

model = chatLLM(model="HuggingFaceTB/SmolLM2-135M") #"C:/Users/Eddy Ejembi/Documents/MODELS/3.2-MODEL")
llm = model.llm()

def generate_sql(query: str, db_type: str, schema: List[dict]) -> str:
    """Generate SQL query from a natural language query."""
    if not query or not db_type or not schema:
        raise ValueError("Query, database type, and schema must be provided.")

    prompt = PromptTemplate(template=SQL_PROMPT_TEMPLATE, input_variables=["query", "db_type", "schema"])
    formatted_prompt = prompt.format(query=query, db_type=db_type, schema=schema)
    print(f"Prompt: {formatted_prompt}")
    print(f"Prompt Length: {formatted_prompt.__len__()}")
    sql_query = llm.invoke(formatted_prompt)
    return str(sql_query)


"""def clean_sql_query(raw_sql: str) -> str:
    # Extract code between ```sql and ```
    match = re.search(r"```sql(.*?)```", raw_sql, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: remove any lines starting with # or triple backticks
    lines = raw_sql.splitlines()
    clean_lines = [line for line in lines if not line.strip().startswith("#") and not line.strip().startswith("```")]
    return "\n".join(clean_lines).strip()"""

def clean_sql_query(raw_sql: str) -> str:
    # Try to extract code between ```sql and ```
    match = re.search(r"```sql(.*?)```", raw_sql, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no code block, extract line(s) after "Action:" up to "Observation:"
    action_match = re.search(r"Action:\s*(.*?)\s*Observation:", raw_sql, re.DOTALL)
    if action_match:
        cleaned = action_match.group(1).strip()
        # Remove any lingering ```sql or ``` from the extracted text
        cleaned = re.sub(r"```sql|```", "", cleaned).strip()
        return cleaned

    # Fallback: remove any lines starting with # and triple backticks
    lines = raw_sql.splitlines()
    clean_lines = [line for line in lines if not line.strip().startswith("#") and not line.strip().startswith("```")]
    return "\n".join(clean_lines).strip()

def execute_query(db_connector, sql_query: str):
    if not db_connector:
        raise ValueError("Database connector is not initialized.")

    try:
        cleaned_sql = clean_sql_query(sql_query)
        print(f"Cleaned SQL Query: {cleaned_sql}")
        result = db_connector.execute_query(cleaned_sql)
        return result
    except Exception as e:
        return {"error": str(e)}


# Equip the Agent with Tools
tools = [
    generate_sql,
    execute_query,
]

#llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)