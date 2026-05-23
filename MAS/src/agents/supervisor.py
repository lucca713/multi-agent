from langchain_google_genai import ChatGoogleGenerativeAI
from src.core.state import AgentState

def supervise_node(state: AgentState) -> dict:
    """
    Agente Supervisor:
    Analisa o estado atual, verifica se há passos restantes no plano e
    decide quem deve ser chamado em seguida (Planner, Executor, ou fim).
    """
    print("--- [Supervisor] Avaliando estado... ---")
    
    current_plan = state.get("current_plan", [])
    history = state.get("history", [])
    mission_status = state.get("mission_status", "in_progress")
    
    # Se não há plano, chama o planejador ou finaliza a missão
    if not current_plan and mission_status == "in_progress":
        if history:
            print("--- [Supervisor] Missão concluída! ---")
            return {"mission_status": "success", "next_node": "END"}
            
        print("--- [Supervisor] Sem plano. Encaminhando para Planner. ---")
        return {"next_node": "planner"}
        
    # Se há um plano, pega o próximo passo
    if current_plan:
        next_step = current_plan.pop(0) # Retira o primeiro passo do plano
        print(f"--- [Supervisor] Despachando passo para Executor: '{next_step}'. Passos restantes: {len(current_plan)} ---")
        
        return {
            "current_step": next_step,
            "current_plan": current_plan, # Atualiza o plano sem o passo que foi despachado
            "next_node": "executor"
        }
        
    # Se não há plano e já não é o começo, a missão terminou (sucesso)
    print("--- [Supervisor] Missão concluída! ---")
    return {"mission_status": "success", "next_node": "END"}
