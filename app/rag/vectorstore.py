from langchain_pinecone import PineconeVectorStore
from app.config import settings
from app.rag.embeddings import get_embeddings_model

def get_vectorstore():

    embeddings= get_embeddings_model()

    vectorstore=PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME, embedding=embeddings, pinecone_api_key=settings.PINECONE_API_KEY
    )
    return vectorstore

def save_to_pinecone(chunks):

    print(f"Subiendo {len(chunks)} pedazos a pinecone")
    
    vectorstore = get_vectorstore()

    vectorstore.add_documents(chunks)
    print("Datos guardados exitosamente en la nube!")