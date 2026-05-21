import streamlit as st
import zipfile
import io

st.set_page_config(page_title="Fotos para WhatsApp", page_icon="📸")
st.title("📸 Enviar Fotos sem Perder Qualidade")
st.write("Suba as fotos da sua galeria e baixe o arquivo ZIP pronto.")

fotos_enviadas = st.file_uploader(
    "Escolha as fotos da sua galeria:", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if fotos_enviadas:
    st.success(f"{len(fotos_enviadas)} foto(s) carregada(s)!")
    buffer_memoria = io.BytesIO()
    
    with zipfile.ZipFile(buffer_memoria, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foto in fotos_enviadas:
            if hasattr(foto, 'name') and hasattr(foto, 'getvalue'):
                zipf.writestr(foto.name, foto.getvalue())
                st.write(f"✔️ {foto.name} adicionada.")
            
    buffer_memoria.seek(0)
    st.markdown("---")
    
    st.download_button(
        label="📥 Baixar arquivo ZIP para o WhatsApp",
        data=buffer_memoria,
        file_name="fotos_alta_qualidade.zip",
        mime="application/zip",
        use_container_width=True
    )
