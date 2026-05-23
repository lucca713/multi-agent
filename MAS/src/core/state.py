import operator
from typing import Annotated, TypedDict, List, Any

class AgentState(TypedDict):
    # A intenção original do usuário (vinda do módulo de PLN)
    user_intent: str
    
    # O plano atual gerado pelo Planejador (lista de strings/passos)
    current_plan: List[str]
    
    # O passo atual que está sendo executado
    current_step: str
    
    # Histórico de execuções ou feedbacks dos nós
    history: Annotated[List[str], operator.add]
    
    # Status da missão: "in_progress", "success", "failed"
    mission_status: str
    
    # Próximo agente a ser chamado pelo Supervisor
    next_node: str
