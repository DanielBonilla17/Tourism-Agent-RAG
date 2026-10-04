import requests
from app.config import settings

def send_whatsapp_message(to_phone:str, message:str):

    url=f"https://graph.facebook.com/v22.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

    headers={
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type":"application/json",
    }

    data={
        "messaging_product":"whatsapp",
        "to":to_phone,
        "type":"text",
        "text":{"body":message},
    }

    try: 
      response= requests.post(url,headers=headers,json=data)
      response.raise_for_status()
      print(f"Mensaje enviado a{to_phone}")
      return response.json()
    except Exception as e:
        print(f"Error enviando mensaje a Whatsapp: {e}")
