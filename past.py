import streamlit as st
import zipfile
import io
import os
from pyngrok import ngrok

# === CONFIGURAÇÃO DO LINK PARA O CELULAR (NGROK) ===
# Executa apenas uma vez ao iniciar o programa
if 'link_criado' not in st.session_state:
    try:
        # Abre um túnel público seguro na porta padrão do Streamlit (8501)
        tunnel = ngrok.connect(8501)
        st.session_state['link_url'] = tunnel.public_url
        st.session_state['link_criado'] = True

        print("\n" + "=" * 60)
        print("🔗 COPIE ESTE LINK E ABRA NO SEU CELULAR:")
        print(f"👉 {tunnel.public_url}")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"Erro ao gerar link do Ngrok: {e}")
        st.session_state['link_url'] = "Erro ao gerar link automaticamente."

# === INTERFACE DO SISTEMA ===
st.set_page_config(page_title="Fotos para WhatsApp", page_icon="📸")
st.title("📸 Compactador de Fotos de Alta Qualidade")

# Exibe o link também no topo da página da web
st.info(f"Link de acesso pelo celular: {st.session_state.get('link_url', 'Carregando...')}")

st.write("Selecione ou arraste as fotos da galeria para criar o lote em ZIP.")

fotos_enviadas = st.file_uploader(
    "Escolha as fotos:",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if fotos_enviadas:
    st.success(f"{len(fotos_enviadas)} foto(s) carregada(s) com sucesso!")
    buffer_memoria = io.BytesIO()

    with zipfile.ZipFile(buffer_memoria, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foto in fotos_enviadas:
            if hasattr(foto, 'name') and hasattr(foto, 'getvalue'):
                zipf.writestr(foto.name, foto.getvalue())
                st.write(f"✔️ {foto.name} pronta.")

    buffer_memoria.seek(0)
    st.markdown("---")

    st.download_button(
        label="📥 Baixar arquivo ZIP para enviar no WhatsApp",
        data=buffer_memoria,
        file_name="fotos_galeria_doc.zip",
        mime="application/zip",
        use_container_width=True
    )
