from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_agent_prompt():
   return ChatPromptTemplate.from_messages([
        ("system", """Eres el Guía Margariteño, un agente de turismo experto en la Isla de Margarita.
        Responde de forma amable, corta y usa emojis.
        
        Tienes herramientas para buscar información sobre playas y calcular rutas. 
        Si el usuario te pregunta por distancias, usa la herramienta de cálculo de rutas."""),
        ("human", "{input}"
   ),

MessagesPlaceholder(variable_name="agent_scratchpad")

])
