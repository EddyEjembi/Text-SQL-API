import os
import dotenv
from huggingface_hub import InferenceClient
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_huggingface.llms  import HuggingFacePipeline, HuggingFaceEndpoint
import torch

dotenv.load_dotenv()


def get_huggingface_client(model_id: str):

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)

    llm_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        device=0 if torch.cuda.is_available() else -1,
        truncation=True
    )
    llm = HuggingFacePipeline(pipeline=llm_pipeline, model_kwargs={"max_new_tokens": 256})
    """llm = HuggingFaceEndpoint(
        repo_id=model_id,
        task="text-generation",
        max_new_tokens=256,
        device=0 if torch.cuda.is_available() else -1,
        truncation=True,
        provider="novita",
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY")
    )"""
    
    return llm

def get_openai_client(model_id: str):
    """
    Get OpenAI client.
    """
    client = InferenceClient(
        repo_id=model_id,
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_KEY")
    )
    return client