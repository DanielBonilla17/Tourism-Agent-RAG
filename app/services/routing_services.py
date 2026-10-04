import requests

url_base = "http://osrm:5000/route/v1/driving/"

def obtener_info_ruta(lon_origen, lat_origen, lon_destino, lat_destino):
    url = f"{url_base}{lon_origen},{lat_origen};{lon_destino},{lat_destino}?overview=false"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("code") == "Ok":
            ruta = data["routes"][0]
            distancia_km = ruta["distance"] / 1000
            duracion_min = ruta["duration"] / 60

            return {
                "distancia": round(distancia_km, 2),
                "tiempo": round(duracion_min)
            }
    except Exception as e:
        print(f"Error consultando OSRM: {e}")
        
    return None

# Prueba rápida
if __name__ == "__main__":
    resultado = obtener_info_ruta(-63.8080, 10.9992, -63.8620, 11.1406)
    if resultado:
        print(f"Estás a {resultado['distancia']} km de distancia")
        print(f"Llegarás en aproximadamente {resultado['tiempo']} minutos en carro")