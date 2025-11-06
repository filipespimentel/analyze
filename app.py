import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

# Caminhos dos arquivos
CONFIG_PATH = Path("config/credentials.yaml")
SERVICES_PATH = Path("config/services.yaml")

# Função: Carregar configurações YAML
def load_yaml(path):
    if not path.exists():
        st.error(f"Arquivo não encontrado: {path}")
        return {}
    with open(path, "r", encoding="utf-8") as file:
        return yaml.load(file, Loader=SafeLoader)

# Função: Páginas
def pagina_irpf():
    st.title("💰 Imposto de Renda (IRPF)")
    st.write("Envie seus documentos e dados para a declaração anual de IRPF.")
    st.file_uploader("Envie seus arquivos (PDF, JPG, DOCX, XLSX):", accept_multiple_files=True)

def pagina_bi():
    st.title("📊 Análise de Dados (BI)")
    st.write("Envie planilhas e relatórios para criar painéis personalizados de Business Intelligence.")
    st.file_uploader("Envie seus arquivos (CSV, XLSX, TXT):", accept_multiple_files=True)

def pagina_pedidos():
    st.title("📦 Meus Pedidos")
    st.write("Aqui você verá o histórico de serviços enviados.")
    st.info("Nenhum pedido encontrado ainda.")

# Função principal
def main():
    st.set_page_config(page_title="RD Serviços", page_icon="🧱", layout="wide")

    # Carregar credenciais
    config = load_yaml(CONFIG_PATH)
    if not config:
        return

    # Criar autenticador (versão nova compatível)
    authenticator = stauth.Authenticate.from_yaml(config)

    # Login
    authenticator.login("main")

    if st.session_state["authentication_status"]:
        authenticator.logout("Sair", "sidebar")
        st.sidebar.title(f"Bem-vindo, {st.session_state['name']} 👋")

        menu = st.sidebar.radio("Navegação", ["🏠 Início", "💰 Imposto de Renda", "📊 Análise de Dados", "📦 Meus Pedidos"])

        if menu == "🏠 Início":
            st.title("🧱 RD Serviços")
            st.write("""
            Bem-vindo à plataforma de serviços da **RD**.

            Escolha uma das opções no menu lateral:
            - 💰 Enviar documentos para **Imposto de Renda**
            - 📊 Solicitar **Análise de Dados**
            - 📦 Acompanhar **Meus Pedidos**
            """)

        elif menu == "💰 Imposto de Renda":
            pagina_irpf()
        elif menu == "📊 Análise de Dados":
            pagina_bi()
        elif menu == "📦 Meus Pedidos":
            pagina_pedidos()

    elif st.session_state["authentication_status"] is False:
        st.error("Usuário ou senha incorretos.")
    elif st.session_state["authentication_status"] is None:
        st.warning("Por favor, insira seu nome de usuário e senha.")

if __name__ == "__main__":
    main()
