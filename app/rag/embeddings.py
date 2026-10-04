from langchain_openai import OpenAIEmbeddings
from app.config import settings


def get_embeddings_model():
    model=OpenAIEmbeddings(
        model="text-embedding-3-small",
   api_key=settings.OPENAI_API_KEY
    )
    return model
