from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings
import sqlite3
import re

def clean_address(address):
    """Elimina los códigos Plus (ej: X5RH+3W8) al inicio de las direcciones."""
    if not address:
        return "No disponible"
    # Regex para detectar códigos plus (letras/números + '+' + letras/números seguidos de coma)
    cleaned = re.sub(r'^[A-Z0-9]{4,8}\+[A-Z0-9]{2,}\s*,\s*', '', address)
    return cleaned

def load_knowledge_base():
    # 1. Cargar archivos .md (playas)
    loader = DirectoryLoader(
        'knowledge_base',
        glob="./*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    docs = loader.load()
    print(f"Archivos MD cargados: {len(docs)} archivos")
    
    # 2. Cargar restaurantes desde SQLite
    db_path = 'knowledge_base/margarita_restaurants.db'
    restaurant_docs = load_restaurants_from_db(db_path)
    docs.extend(restaurant_docs)
    
    print(f"Total de documentos cargados para el Agente: {len(docs)}")
    return docs

def load_restaurants_from_db(db_path):
    """Lee la base de datos SQLite y convierte cada restaurante en un Document."""
    docs = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, address, rating, latitude, longitude, category FROM restaurants")
        rows = cursor.fetchall()
        
        for row in rows:
            name, address, rating, lat, lon, category = row
            
            # Limpiamos la dirección
            direccion_limpia = clean_address(address)
            
            # Formateamos el texto
            texto = f"Restaurante: {name}\n"
            texto += f"Categoría: {category}\n"
            texto += f"Dirección: {direccion_limpia}\n"
            texto += f"Rating: {rating} estrellas\n"
            if lat and lon:
                texto += f"📍 Coordenadas: {lat}, {lon}\n"
            
            docs.append(Document(
                page_content=texto, 
                metadata={"source": "margarita_restaurants.db", "name": name}
            ))
            
        conn.close()
        print(f"✅ {len(docs)} restaurantes cargados y limpiados desde la base de datos.")
    except Exception as e:
        print(f"❌ Error cargando restaurantes: {e}")
        
    return docs

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Se crearon {len(chunks)} pedazos (chunks) de texto")
    return chunks
