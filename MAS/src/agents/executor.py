from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from src.core.state import AgentState

# Importar as ferramentas reais do ROS 2 legado
from robot_tools import (
    navigate_to, 
    pick_up_object, 
    search_for_object, 
    find_object, 
    deliver_object,
    find_person,
    update_person_location
)

# Lista de ferramentas que o Executor terá à disposição
ROS2_TOOLS = [
    navigate_to, 
    pick_up_object, 
    search_for_object, 
    find_object, 
    deliver_object,
    find_person,
    update_person_location
]

def execute_node(state: AgentState) -> dict:
    """
    Agente de Execução:
    Recebe um único passo do Supervisor e o executa usando as ferramentas Langchain conectadas ao ROS 2.
    """
    print("--- [Executor] Trabalhando... ---")
    
    current_step = state.get("current_step")
    print(f"--- [Executor] Traduzindo passo para ação real: '{current_step}' ---")
    
    # Inicializando o LLM do Gemini para o agente ReAct
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Cria o agente ReAct que tem acesso às ferramentas ROS 2
    react_agent = create_react_agent(llm, tools=ROS2_TOOLS)
    
    # Executa o agente passando o passo como mensagem humana
    # Adicionamos uma instrução extra para garantir que ele chame as ferramentas
    prompt = f"Por favor, execute a seguinte ação usando suas ferramentas de hardware. Apenas execute a ação, não explique muito: {current_step}"
    
    try:
        result = react_agent.invoke({"messages": [HumanMessage(content=prompt)]})
        # A última mensagem contém a resposta final do LLM
        final_message = result["messages"][-1].content
        feedback_status = "success"
        feedback_msg = final_message
    except Exception as e:
        feedback_status = "failed"
        feedback_msg = str(e)
        print(f"--- [Executor] Erro na execução: {e} ---")
    
    print(f"--- [Executor] Feedback do ambiente: {feedback_status} | Resposta: {feedback_msg} ---")
    
    return {
        "history": [f"Executado: {current_step} -> {feedback_status} ({feedback_msg})"]
    }
