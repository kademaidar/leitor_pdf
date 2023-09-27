import streamlit as st
import my_functions as mf


st.title("AutoPDF !")

pdfs_list = st.file_uploader(
    "Arraste os PDFs", type=["pdf"], accept_multiple_files=True
)

if len(pdfs_list) == 0:
    st.warning("Insira seus PDFs")
else:
    pdfs_text_list = mf.read_pdfs(pdfs_list)

    st.success(f"Parabens, vc colocou {len(pdfs_list)} arquivos PDF !")

    for pdf_text in pdfs_text_list:
        topic_list = mf.split_into_topics(pdf_text)

        answers_list = []

        answers_list.extend(mf.get_topic_3_data(topic_list[3]))
        answers_list.extend(mf.get_topic_4_data(topic_list[4]))
        answers_list.extend(mf.get_topic_5_data(topic_list[5]))

        mf.tester(answers_list)

        # answer = mf.funcao(topic_list)

        # st.write(f"ORIGEM: {answer}")
