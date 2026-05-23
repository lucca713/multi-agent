import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório do sistema legado ao PATH do Python
LEGACY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ros2_ws_victor", "robot-agent", "ros2_ws", "src", "robot_agent"))
if LEGACY_DIR not in sys.path:
    sys.path.append(LEGACY_DIR)

# Agora podemos importar o módulo legado
from robot_tools import init_ros_node

from src.core.graph import build_graph

# Carrega as variáveis de ambiente (como GEMINI_API_KEY) do arquivo .env
# Assumindo que seu arquivo se chama .env e está na pasta config
load_dotenv(dotenv_path="config/.env")

def main():
    print("Iniciando o Sistema Multi-Agente (LangGraph)...")
    
    # Inicializa o nó do ROS 2 do sistema legado
    print("Inicializando nó ROS 2...")
    init_ros_node()
    
    # Verifica se a chave da API foi carregada (o LangChain Google vai usar GOOGLE_API_KEY)
    if "GOOGLE_API_KEY" not in os.environ:
        print("AVISO: GOOGLE_API_KEY não encontrada nas variáveis de ambiente.")
        print("Certifique-se de que o arquivo config/.env possui essa variável.")
    
    # Construir a aplicação (grafo)
    app = build_graph()
    
    # Definindo a intenção inicial do usuário
    user_intent = "Vá à cozinha, encontre Ana e diga olá."
    
    print(f"\n--- Intenção do Usuário: '{user_intent}' ---\n")
    
    # Estado inicial
    initial_state = {
        "user_intent": user_intent,
        "current_plan": [],
        "current_step": "",
        "history": [],
        "mission_status": "in_progress",
        "next_node": ""
    }
    
    # Executando o grafo
    # stream() permite iterar por cada passo/nó do grafo
    for s in app.stream(initial_state):
        # s é um dicionário com a chave sendo o nome do nó e o valor sendo a atualização do estado
        node_name = list(s.keys())[0]
        print(f"--- [MAIN] Nó '{node_name}' finalizou ---")
        
if __name__ == "__main__":
    main()
