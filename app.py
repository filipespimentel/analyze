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


def load_credentials():
    """Carrega as credenciais de usuários do arquivo YAML."""
    if not CREDENTIALS_PATH.exists():
        st.error(f"Arquivo de credenciais não encontrado: {CREDENTIALS_PATH}")
        return None
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_app(authenticator):
    """Função que contém o conteúdo principal do aplicativo Streamlit."""

    # Título principal
    st.title("🧱 RD Serviços")

    # Carrega a configuração para garantir que as páginas sejam exibidas corretamente
    services_config = load_config()
    st.session_state["services_config"] = services_config

    # Sidebar com boas-vindas e botão de logout
    st.sidebar.subheader(f"Bem-vindo, {st.session_state['name']}")
    if st.sidebar.button("Sair"):
        authenticator.logout(location="sidebar")

    # Conteúdo principal
    st.markdown(
        """
        Bem-vindo à plataforma de envio de documentos da **RD Serviços**.
        
        Use o menu lateral para selecionar o serviço desejado:
        
        - **Imposto de Renda (IRPF)**: Envie seus documentos para a declaração anual.
        - **Análise de Dados (BI)**: Descreva sua necessidade e envie suas bases de dados.
        
        Seu envio será organizado e salvo localmente em `data/uploads/` para processamento futuro.
        """
    )


def main():
    st.set_page_config(
        page_title="RD Serviços - Login",
        page_icon="🧱",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # 1. Carregar credenciais
    credentials_config = load_credentials()
    if not credentials_config:
        return

    # 2. Configurar o autenticador (versão atualizada)
    authenticator = stauth.Authenticate(
        credentials=credentials_config["credentials"],
        cookie_name=credentials_config["cookie"]["name"],
        key=credentials_config["cookie"]["key"],
        cookie_expiry_days=credentials_config["cookie"]["expiry_days"],
    )

    # 3. Exibir a tela de login
    name, authentication_status, username = authenticator.login(
        "Login", location="main"
    )

    if authentication_status:
        # Usuário logado
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
