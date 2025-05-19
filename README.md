# 📖 Text-to-SQL API

A lightweight, agent-based Text-to-SQL system. This API lets users connect to supported databases, run raw SQL queries, or ask natural language questions that get converted to SQL using an agent workflow powered by LLMs.

## 📌 Features
✅ Connect/Disconnect to Databases (currently supports SQLite, with Postgres scaffolded)

✅ Natural Language to SQL Conversion using LLM agents.

✅ Multi-Provider Model Support — bring your own OpenAI, Gemini, or other LangChain-compatible models.

✅ Tool-Driven Workflow for listing tables, getting schemas, validating, and executing queries.

✅ FastAPI-powered REST API interface for integration.


## 📡 API Endpoints

|Method|Endpoint|Description|
|------|--------|-----------|
|`GET`|/|API healthcheck and available actions overview|
|`POST`|/connect|Connect to a database
|`POST`|/sql-query|Execute a raw SQL query against the connected database|
|`POST`|/query|Submit a natural language question to the agent for SQL generation|
|`POST`|/disconnect|Disconnect from the active database|


### 📊 Root Endpoint Response
When you `GET /`, you'll see an overview of your API’s capabilities:

```
{
  "message": "Database Connector API is running",
  "available_databases": ["sqlite", "postgres"],
  "To Connect": "POST /connect",
  "To Disconnect": "POST /disconnect",
  "To Execute SQL": "POST /sql-query",
  "To Execute SQL with Agent": "POST /query",
  "Query Payload": {
    "question": "What is the question?",
    "model": "Select a model (e.g., 'gemini-2.0-flash')",
    "provider": "Select a provider (e.g., 'google_genai')",
    "api_key": "your_api_key"
  },
  "Query Note": "Install the required LangChain package for your model provider. E.g., 'google_genai' requires 'langchain-google', openai requires 'langchain-openai', etc."
}
```

### 🚀 How It Works
#### Natural Language Query Flow
1. Connect to a database via `POST /connect`
2. Submit a question via POST /query with the required payload:
- `question`: Natural language question
- `model`: Model name (e.g., gemini-2.0-flash)
- `provider`: LangChain-supported provider (e.g., google_genai, openai)
- `api_key`: API key for the selected provider
3. Returns structured result

## 🛠️ Setup & Run
### Clone Repository
```
git clone https://github.com/EddyEjembi/Text-SQL-API.git
cd Text-SQL-API
```

#### 🔗 Install Dependencies
```
pip install -r requirements.txt
```

📌 Note: Ensure to install any additional LangChain integrations (e.g., langchain-google, langchain-openai) are installed if you're using their respective providers.

#### 🖥️ Run API Server
```
uvicorn api.server:app --reload
```

# Connect With Me
connect with me on any of the platform:

- 🐦[ X (Twitter)](https://x.com/eddyejembi)
- 💼[ LinkedIn](https://www.linkedin.com/in/eddyejembi/)
- 📬[ Mail](mailto:eddyejembi2018@gmail.com)
