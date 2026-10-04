import re
from langchain_core.tools import tool
from app.services.routing_services import obtener_info_ruta
from app.rag.vectorstore import get_vectorstore

def extraer_coordenadas(texto: str):
    match = re.search(r"📍.*?([0-9.-]+),\s*([0-9.-]+)", texto)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

@tool
def calcular_ruta_osrm(lugar_origen: str, lugar_destino: str, lat_secreta: float = 0.0, lon_secreta: float = 0.0) -> str:
    """
    Calcula la distancia en kilómetros y el tiempo en auto entre dos lugares de Isla Margarita.
    - Si el origen es la ubicación actual del usuario, pasa lugar_origen="UBICACION_USUARIO" y pon las coordenadas en lat_secreta y lon_secreta.
    - Si son lugares turísticos (ej. "Playa Parguito", "Restaurante La Mar"), NO pases lat_secreta ni lon_secreta. Solo pasa el nombre. La herramienta buscará sus coordenadas automáticamente.
    """
    vectorstore = get_vectorstore()
    
    # Obtener coordenadas de origen
    if lugar_origen == "UBICACION_USUARIO" and lat_secreta != 0.0:
        lat_o, lon_o = lat_secreta, lon_secreta
    else:
        docs = vectorstore.similarity_search(lugar_origen, k=2)
        lat_o, lon_o = None, None
        for d in docs:
            lat_o, lon_o = extraer_coordenadas(d.page_content)
            if lat_o: break
        if not lat_o:
            return f"No encontré coordenadas para el lugar de origen: {lugar_origen}."

    # Obtener coordenadas de destino
    if lugar_destino == "UBICACION_USUARIO" and lat_secreta != 0.0:
        lat_d, lon_d = lat_secreta, lon_secreta
    else:
        docs = vectorstore.similarity_search(lugar_destino, k=2)
        lat_d, lon_d = None, None
        for d in docs:
            lat_d, lon_d = extraer_coordenadas(d.page_content)
            if lat_d: break
        if not lat_d:
            return f"No encontré coordenadas para el lugar de destino: {lugar_destino}."

    print(f"\n[DEBUG TOOL] Ruta automatizada: ({lat_o},{lon_o}) a ({lat_d},{lon_d})\n", flush=True)
    
    # OSRM espera (lon, lat)
    resultado = obtener_info_ruta(lon_o, lat_o, lon_d, lat_d)
    
    if resultado:
        return f"Ruta exitosa. Distancia: {resultado['distancia']} km. Tiempo estimado: {resultado['tiempo']} minutos en auto."
    return "Error en el servidor OSRM al calcular la ruta."
