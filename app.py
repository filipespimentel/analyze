import streamlit as st
import streamlit_authenticator as stauth
import yaml
from pathlib import Path

# Caminhos
CONFIG_PATH = Path("config/services.yaml")
CREDENTIALS_PATH = Path("config/credentials.yaml")
UPLOADS_DIR = Path("data/uploads")

# Funções auxiliares
def load_config():
    if not CONFIG_PATH.exists():
        st.error(f"Arquivo não encontrado: {CONFIG_PATH}")
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_credentials():
    if not CREDENTIALS_PATH.exists():
        st.error(f"Arquivo não encontrado: {CREDENTIALS_PATH}")
        return None
    with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run_app(authenticator):
    st.title("🧱 RD Serviços")
    st.sidebar.subheader(f"Bem-vindo, {st.session_state['name']}")
    if st.sidebar.button("Sair"):
        authenticator.logout("Logout", "sidebar")

    services_config = load_config()
    st.session_state["services_config"] = services_config

    st.markdown("""
    ### Portal de Serviços RD

    Escolha o serviço desejado:

    - 💰 **Imposto de Renda (IRPF)**
    - 📊 **Análise de Dados (BI)**
    - 📁 **Consultoria Contábil**
    """)

def main():
    st.set_page_config(page_title="RD Serviços", page_icon="🧱")

    # Carregar credenciais
    credentials_config = load_credentials()
    if not credentials_config:
        return

    # Configurar autenticação (modo compatível)
    authenticator = stauth.Authenticate(
        credentials_config["credentials"],
        credentials_config["cookie"]["name"],
        credentials_config["cookie"]["key"],
        credentials_config["cookie"]["expiry_days"],
        credentials_config.get("preauthorized")
    )

    # Login (sem 'location', compatível com versões antigas)
    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.session_state["authentication_status"] = authentication_status
        st.session_state["name"] = name
        st.session_state["username"] = username
        run_app(authenticator)

    elif authentication_status is False:
        st.error("Nome de usuário ou senha incorretos.")
    elif authentication_status is None:
        st.warning("Por favor, insira suas credenciais.")

if __name__ == "__main__":
    main()
