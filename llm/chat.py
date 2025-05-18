from langchain.chat_models import init_chat_model
from llm.client import get_huggingface_client

class HuggingFaceLLM:
    """
    Chat with a HuggingFace Language Model.
    """
    def __init__(self, model: str):
        self.model = model

    def llm(self,):
        client = get_huggingface_client(self.model)
        return client
    
class ChatLLM:
    """
    Chat with an API Language Model.
    """
    def __init__(self, model: str, provider: str, api_key: str):
        self.model = model
        self.provider = provider
        self.api_key = api_key

    def llm(self,):
        client = init_chat_model(self.model, model_provider=self.provider, api_key=self.api_key)
        return client
    