from app.agent.chain import agent_executor
from app.services.whatsapp_service import send_whatsapp_message

# Inicializamos el diccionario para recordar la ubicación de cada usuario
ubicaciones_usuarios = {}

async def handle_whatsapp_message(data):
    """
    Procesa el JSON de WhatsApp, extrae el mensaje y responde.
    """
    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return
            
        message = messages[0]
        from_phone = message.get("from")
        message_type = message.get("type", "text")
        # --- 1. SI ENVÍA UBICACIÓN ---
        if message_type == "location":
            lat = message.get("location", {}).get("latitude")
            lon = message.get("location", {}).get("longitude")
            
            # Guardamos la ubicación en nuestro diccionario usando el teléfono como llave
            ubicaciones_usuarios[from_phone] = {"lat": lat, "lon": lon}
            print(f"📍 Ubicación guardada de {from_phone}: {lat}, {lon}")
            
            respuesta = "¡Ubicación recibida! 📍 Ahora puedo calcular la distancia y el tiempo a tus destinos favoritos. ¿A qué playa o restaurante te gustaría ir?"
            send_whatsapp_message(from_phone, respuesta)
            return
            
        # --- 2. SI ENVÍA TEXTO ---
        message_text = message.get("text", {}).get("body", "")
        if not message_text:
            return
            
        print(f"👤 Pregunta de {from_phone}: {message_text}")
        
        # Le inyectamos la ubicación al LLM si la tenemos guardada
        contexto_ubicacion = ""
        if from_phone in ubicaciones_usuarios:
            user_loc = ubicaciones_usuarios[from_phone]
            contexto_ubicacion = f"\n\n[INFO DE CONTEXTO SECRETA: El usuario está actualmente en las coordenadas Latitud: {user_loc['lat']}, Longitud: {user_loc['lon']}]."
            
        texto_para_llm = message_text + contexto_ubicacion
        
        # Llamamos al Agente (nueva API: usa "messages" en vez de "input")
        resultado = agent_executor.invoke(
            {"messages": [{"role": "user", "content": texto_para_llm}]},
            config={"configurable":{"thread_id":from_phone}}
        )
        # Extraemos el último mensaje del agente
        response = resultado["messages"][-1].content
        
        # Enviamos la respuesta de vuelta por WhatsApp
        send_whatsapp_message(from_phone, response)
        
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")
