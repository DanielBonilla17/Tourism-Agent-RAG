import sys
import os

# Agregamos la raíz al PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent.chain import get_rag_chain

def chat():
    print("🏝️ BIENVENIDO A MARGARITA, COMPAI! (Escribe 'salir' para terminar)")
    
    # Inicializamos la cadena
    chain = get_rag_chain()
    
    while True:
        pregunta = input("\n👤 Tú: ")
        
        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("👋 ¡Vuelva pronto, mijo! ¡Se me cuida!")
            break
            
        print("🤔 Pensando como margariteño...")
        
        # Ejecutamos la cadena
        # La respuesta viene en un diccionario, la respuesta real está en 'answer'
        response = chain.invoke({"input": pregunta})
        
        print(f"\n🦜 Guía: {response}")
if __name__ == "__main__":
    chat()
