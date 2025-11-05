import streamlit as st
import yaml
from pathlib import Path
from datetime import datetime
import glob

# Diretório de uploads
UPLOADS_DIR = Path("data/uploads")

def load_pedido_metadata(metadata_path):
    """Carrega os metadados de um pedido do arquivo YAML."""
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        st.error(f"Erro ao ler metadados em {metadata_path}: {e}")
        return None

def meus_pedidos_page():
    # Proteção de login
    if not st.session_state.get('authentication_status'):
        st.warning("Por favor, faça login na página inicial para acessar este serviço.")
        return

    st.title("📦 Meus Pedidos")
    st.markdown(f"Histórico de envios para o usuário **{st.session_state.get('username')}**.")

    current_username = st.session_state.get('username')
    pedidos_list = []

    # 1. Buscar todos os arquivos metadata.yaml nos subdiretórios de UPLOADS_DIR
    # Usamos glob para buscar recursivamente em todos os subdiretórios de serviço (IRPF, BI)
    # e subdiretórios de pedido (cpf_ano_timestamp, pedido_timestamp)
    
    # A função glob.glob é mais fácil de usar com strings de caminho.
    # O padrão é: data/uploads/*/*/metadata.yaml
    search_pattern = str(UPLOADS_DIR / "**" / "metadata.yaml")
    
    # O glob.glob não funciona bem com Path.glob() em alguns ambientes, então usaremos o módulo glob
    # para garantir a compatibilidade e a busca recursiva.
    # No entanto, vamos usar Path.rglob() que é a forma mais moderna e Pythonica.
    
    for metadata_path in UPLOADS_DIR.rglob("metadata.yaml"):
        metadata = load_pedido_metadata(metadata_path)
        
        if metadata and metadata.get('username') == current_username:
            # Formatar os dados para exibição
            pedido_data = {
                "Serviço": metadata.get('service', 'N/A'),
                "Data/Hora": datetime.strptime(metadata.get('timestamp'), "%Y%m%d_%H%M%S").strftime("%d/%m/%Y %H:%M:%S"),
                "Descrição": metadata.get('descricao', metadata.get('nome', 'N/A')), # Usa 'descricao' para BI e 'nome' para IRPF
                "Arquivos": len(metadata.get('files', [])),
                "Pasta": str(metadata_path.parent.relative_to(UPLOADS_DIR))
            }
            pedidos_list.append(pedido_data)

    if not pedidos_list:
        st.info("Você ainda não tem pedidos enviados.")
        return

    # 2. Exibir os pedidos em uma tabela
    pedidos_df = pd.DataFrame(pedidos_list)
    
    # Reordenar as colunas para melhor visualização
    column_order = ["Serviço", "Data/Hora", "Descrição", "Arquivos", "Pasta"]
    pedidos_df = pedidos_df[column_order]

    st.dataframe(pedidos_df, use_container_width=True, hide_index=True)

meus_pedidos_page()
