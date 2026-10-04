from langchain.agents import create_agent
from app.config import settings
from app.agent.tools import calcular_ruta_osrm
from langgraph.checkpoint.redis import RedisSaver
from redis import Redis


def get_rag_agent():

    # 1. Creamos la memoria a corto plazo en Redis
    redis_client = Redis(host="redis", port=6379, db=0)
    memoria_redis= RedisSaver(redis_client=redis_client)
    memoria_redis.setup()

    # 2. Creamos el Agente con la herramienta automatizada
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[calcular_ruta_osrm],
        system_prompt="""Eres un Guía Margariteño experto en la Isla de Margarita. Responde de forma amable, corta y usa emojis.
Si el usuario te pide una distancia o tiempo de viaje entre dos lugares, usa la herramienta 'calcular_ruta_osrm' enviándole los NOMBRES de los lugares (ej. lugar_origen="Playa Parguito", lugar_destino="Restaurante La Mar"). 
La herramienta buscará automáticamente las coordenadas y calculará la ruta.

CONTEXTO DE UBICACIÓN:
Si recibes INFO DE CONTEXTO SECRETA con las coordenadas del usuario, úsalas como origen ÚNICAMENTE si el usuario pregunta explícitamente "cómo llego a..." o "a qué distancia estoy". Para ello, pasa lugar_origen="UBICACION_USUARIO" a la herramienta y envíale las coordenadas secretas. Si menciona dos lugares distintos, ignora tu contexto secreto y pasa solo los nombres.""",
        checkpointer=memoria_redis,
        debug=True
    )
    return agent

# Exportar el agente para que message_handler lo pueda importar
agent_executor = get_rag_agent()
