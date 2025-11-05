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

def irpf_page():
    if not st.session_state.get('authentication_status'):
        st.warning("Por favor, faça login na página inicial para acessar este serviço.")
        return
    st.title("💰 Imposto de Renda (IRPF)")
    st.markdown("Preencha o formulário abaixo e envie seus documentos para a declaração.")

    # Acessa a configuração de serviços
    services_config = st.session_state.get('services_config', {})
    service_name = "IRPF"
    config = services_config.get(service_name, {})

    if not config:
        st.warning(f"Configuração para o serviço '{service_name}' não encontrada. Verifique `config/services.yaml`.")
        return

    with st.form(key=service_name):
        st.subheader("Dados do Contribuinte")
        
        # Campos dinâmicos (Nome, CPF, Ano)
        # Assumindo que os campos são definidos na configuração YAML, mas para simplificar, vamos hardcodar os essenciais
        nome = st.text_input("Nome Completo", key="nome")
        cpf = st.text_input("CPF (somente números)", max_chars=11, key="cpf")
        ano = st.selectbox("Ano de Referência", options=list(range(datetime.now().year, 2018, -1)), key="ano")

        st.subheader("Envio de Documentos")
        
        # Upload de múltiplos arquivos
        allowed_types = config.get('allowed_types', ['pdf', 'xlsx', 'csv'])
        file_uploader_label = f"Selecione os arquivos ({', '.join(allowed_types).upper()})"
        uploaded_files = st.file_uploader(
            file_uploader_label, 
            type=allowed_types, 
            accept_multiple_files=True,
            key="uploaded_files"
        )
        
        submit_button = st.form_submit_button(label="Enviar Documentos")

    if submit_button:
        if not nome or not cpf or not uploaded_files:
            st.error("Por favor, preencha o Nome, CPF e envie pelo menos um arquivo.")
            return

        # 1. Criar pasta de destino
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Formato da pasta: data/uploads/IRPF/CPF_ANO_TIMESTAMP
        upload_folder_name = f"{cpf}_{ano}_{timestamp}"
        target_dir = UPLOADS_DIR / service_name / upload_folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Salvar metadados
        metadata = {
            "service": service_name,
            "username": st.session_state.get('username'), # Adiciona o username
            "nome": nome,
            "cpf": cpf,
            "ano": ano,
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
            st.success(f"Sucesso! Seu pedido de IRPF foi salvo em: `{target_dir.relative_to(Path.cwd())}`")
            st.balloons()
        else:
            st.error("Ocorreu um erro ao salvar um ou mais arquivos. Tente novamente.")

irpf_page()
