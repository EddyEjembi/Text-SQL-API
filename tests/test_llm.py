import os
import dotenv
from llm.chat import chatLLM

dotenv.load_dotenv()

model = chatLLM("C:/Users/Eddy Ejembi/Documents/MODELS/3.2-MODEL")

message = "What is the largest city in Africa?"

client = model.llm()

messages = [
    {
        "role": "user",
        "content": message,
    }
]

response = client.invoke(message)

print(response)