import streamlit as st
import streamlit_authenticator as stauth
import yaml
from pathlib import Path

# Caminhos dos arquivos de configuração
CONFIG_PATH = Path("config/services.yaml")
CREDENTIALS_PATH = Path("config/credentials.yaml")
UPLOADS_DIR = Path("data/uploads")


def load_config():
    """Carrega a configuração de serviços do arquivo YAML."""
    if not CONFIG_PATH.exists():
        st.error(f"Arquivo de configuração não encontrado: {CONFIG_PATH}")
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_app(authenticator):
    """Conteúdo principal do aplicativo após login."""
    st.title("🧱 RD Serviços")

    # Carregar e armazenar configuração de serviços
    services_config = load_config()
    st.session_state["services_config"] = services_config

    # Sidebar de boas-vindas e logout
    st.sidebar.subheader(f"Bem-vindo, {st.session_state['name']}")
    authenticator.logout("Sair", location="sidebar")

    st.markdown(
        """
        Bem-vindo à plataforma de envio de documentos da **RD Serviços**.
        
        Use o menu lateral para selecionar o serviço desejado:
        
        - **Imposto de Renda (IRPF)**: Envie seus documentos para a declaração anual.
        - **Análise de Dados (BI)**: Descreva sua necessidade e envie suas bases de dados.
        
        Seus envios serão organizados e salvos localmente em `data/uploads/` para processamento futuro.
        """
    )


def main():
    st.set_page_config(
        page_title="RD Serviços - Login",
        page_icon="🧱",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # 1️⃣ Carregar credenciais
    if not CREDENTIALS_PATH.exists():
        st.error("Arquivo de credenciais não encontrado em config/credentials.yaml")
        return

    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    # 2️⃣ Detectar versão do streamlit-authenticator
    authenticator = None
    try:
        # Tentativa com nova API (>=0.3.1)
        authenticator = stauth.Authenticate.from_yaml(config)
    except AttributeError:
        # Fallback para versões antigas
        st.warning("Usando modo compatível com versão antiga do streamlit-authenticator.")
        credentials = config["credentials"]
        cookie = config["cookie"]
        authenticator = stauth.Authenticate(
            credentials,
            cookie["name"],
            cookie["key"],
            cookie["expiry_days"],
        )

    # 3️⃣ Tela de login
    name, authentication_status, username = authenticator.login("Login", location="main")

    # 4️⃣ Fluxo de autenticação
    if authentication_status:
        st.session_state["authentication_status"] = authentication_status
        st.session_state["name"] = name
        st.session_state["username"] = username
        run_app(authenticator)

    elif authentication_status is False:
        st.error("Nome de usuário ou senha incorretos")

    elif authentication_status is None:
        st.warning("Por favor, insira seu nome de usuário e senha")


if __name__ == "__main__":
    main()
