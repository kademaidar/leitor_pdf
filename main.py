import streamlit as st


st.title("AutoPDF !")

lista_pdfs = st.file_uploader(
    "Arraste os PDFs", type=["pdf"], accept_multiple_files=True
)

if len(lista_pdfs) > 0:
    st.success(f"Parabens, vc colocou {len(lista_pdfs)} arquivos PDF !")
else:
    st.warning("Insira seus PDFs")