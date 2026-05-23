from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.state import AgentState

def plan_node(state: AgentState) -> dict:
    """
    Agente de Planejamento:
    Recebe o estado com a intenção do usuário ou um feedback de falha,
    e gera um plano de passos para ser executado.
    """
    print("--- [Planejador] Trabalhando... ---")
    
    intent = state.get("user_intent")
    history = state.get("history", [])
    
    # Inicializando o LLM do Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = f"""
    Você é o Agente de Planejamento de um robô de serviço doméstico.
    A intenção do usuário é: "{intent}"
    Histórico recente: {history}
    
    Decomponha essa tarefa em uma lista de subtarefas lógicas sequenciais.
    Responda APENAS com a lista de passos separados por vírgula, sem explicações adicionais.
    Exemplo: "ir para a cozinha, procurar Ana, falar com Ana"
    """
    
    response = llm.invoke(prompt)
    
    # Processando a resposta do LLM para criar uma lista
    plan_text = response.content.strip()
    plan_list = [step.strip() for step in plan_text.split(',')]
    
    print(f"--- [Planejador] Novo Plano Gerado: {plan_list} ---")
    
    return {"current_plan": plan_list}
