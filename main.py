import streamlit as st

import run_apps as run


st.header("Projeto APAS", divider="rainbow")
st.subheader(
    ":red[A]utomação no :orange[P]reenchimento e :green[A]nálise de :blue[S]inistros"
)
st.subheader("")

files_list = st.file_uploader(
    "Arraste seus arquivos aqui",
    type=["pdf", "xlsx"],
    accept_multiple_files=True,
    help="PDF: Coloque quantas Prévias quiser, cuidado para não repetir\n\nEXCEL: Coloque uma planilha do PowerBI e uma dos Embarques (Atenção para que sejam do mesmo período)",
)

extensions_list = [file.name[-1].upper() for file in files_list]
num_extensions = len(set(extensions_list))

if num_extensions == 0:
    st.info("Para começar, coloque seus PDFs de Sinistros ou tabelas de Excel")
elif num_extensions >= 2:
    st.warning("Não misture tipos de arquivos")
else:
    if extensions_list[0] == "F":  # Caso seja PDF
        st.success(f"{len(files_list)} PDFs inseridos !")
        run.pdf_app(files_list)
        st.toast("Seus arquivos foram convertidos!")
    elif extensions_list[0] == "X":  # Caso seja Excel
        st.success(f"{len(files_list)} arquivos Excel inseridos !")
        if len(files_list) < 2:
            st.warning("Insira as duas tabelas necessárias.")
        elif len(files_list) > 2:
            st.warning("Insira apenas as duas tabelas necessárias.")
        else:
            run.excel_app(files_list)
            st.toast("Seus arquivos foram convertidos!")

# st.balloons()
