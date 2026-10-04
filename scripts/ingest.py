import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.loader import split_documents

from app.rag.loader import load_knowledge_base

from app.rag.vectorstore import save_to_pinecone

def run_ingestion():
    print("Iniciando proceso de ingestion")

    docs=load_knowledge_base()

    chunks=split_documents(docs)

    save_to_pinecone(chunks)

    print("Proceso terminado")

if __name__ == "__main__":
    run_ingestion()