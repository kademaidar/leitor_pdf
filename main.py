import streamlit as st
import functions as f


st.title("AutoPDF !")

lista_pdfs = st.file_uploader(
    "Arraste os PDFs", type=["pdf"], accept_multiple_files=True
)

if len(lista_pdfs) == 0:
    st.warning("Insira seus PDFs")
else:
    text = f.read_pdf(lista_pdfs[0])

    st.success(f"Parabens, vc colocou {len(lista_pdfs)} arquivos PDF !")

    st.write(text)
