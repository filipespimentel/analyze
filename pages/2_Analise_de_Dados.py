import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import os

# Diretórios de upload definidos no app.py
UPLOADS_DIR = Path("data/uploads")

def save_uploaded_file(uploaded_file, upload_path):
    """Salva um arquivo enviado pelo usuário no caminho especificado."""
    try:
        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error(f"Erro ao salvar o arquivo: {e}")
        return False

def bi_page():
    if not st.session_state.get('authentication_status'):
        st.warning("Por favor, faça login na página inicial para acessar este serviço.")
        return
    st.title("📊 Análise de Dados (BI)")
    st.markdown("Descreva sua necessidade e envie suas bases de dados (planilhas).")

    # Acessa a configuração de serviços
    services_config = st.session_state.get('services_config', {})
    service_name = "BI"
    config = services_config.get(service_name, {})

    if not config:
        st.warning(f"Configuração para o serviço '{service_name}' não encontrada. Verifique `config/services.yaml`.")
        return

    with st.form(key=service_name):
        st.subheader("Detalhes do Pedido")
        
        # Campo de Descrição do Pedido
        descricao = st.text_area("Descrição do Pedido (O que você precisa que seja analisado?)", key="descricao")

        st.subheader("Bases de Dados")
        
        # Upload de múltiplos arquivos
        allowed_types = config.get('allowed_types', ['csv', 'xlsx'])
        file_uploader_label = f"Selecione as planilhas ({', '.join(allowed_types).upper()})"
        uploaded_files = st.file_uploader(
            file_uploader_label, 
            type=allowed_types, 
            accept_multiple_files=True,
            key="uploaded_files"
        )
        
        submit_button = st.form_submit_button(label="Enviar Pedido")

    if submit_button:
        if not descricao or not uploaded_files:
            st.error("Por favor, preencha a Descrição do Pedido e envie pelo menos uma planilha.")
            return

        # 1. Criar pasta de destino
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Formato da pasta: data/uploads/BI/DESCRICAO_TIMESTAMP
        # Usamos um hash simples do timestamp para garantir unicidade e evitar nomes de pasta muito longos
        upload_folder_name = f"pedido_{timestamp}"
        target_dir = UPLOADS_DIR / service_name / upload_folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Salvar metadados
        metadata = {
            "service": service_name,
            "username": st.session_state.get('username'), # Adiciona o username
            "descricao": descricao,
            "timestamp": timestamp,
            "files": [f.name for f in uploaded_files]
        }
        metadata_path = target_dir / "metadata.yaml"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(metadata, f, allow_unicode=True)

        # 3. Salvar arquivos
        all_saved = True
        for uploaded_file in uploaded_files:
            file_path = target_dir / uploaded_file.name
            if not save_uploaded_file(uploaded_file, file_path):
                all_saved = False
                break
        
        if all_saved:
            st.success(f"Sucesso! Seu pedido de BI foi salvo em: `{target_dir.relative_to(Path.cwd())}`")
            st.balloons()
        else:
            st.error("Ocorreu um erro ao salvar um ou mais arquivos. Tente novamente.")

bi_page()
