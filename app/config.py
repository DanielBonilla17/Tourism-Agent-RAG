import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:

    #OPENAI---------------------------------------
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   
    #PINECONE------------------9ii
    # -------------------
    PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")

    PINECONE_INDEX_NAME= os.getenv("PINECONE_INDEX_NAME")
 
    #WHATSAPP------------------------------------
    WHATSAPP_ACCESS_TOKEN=os.getenv("WHATSAPP_TOKEN")
    
    WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

    WHATSAPP_PHONE_NUMBER_ID=os.getenv("WHATSAPP_PHONE_ID")


    #----PARAMETROS RAG-----------------

    CHUNK_SIZE=500

    CHUNK_OVERLAP=50

    RETRIEVER_K=3


settings=Settings()
