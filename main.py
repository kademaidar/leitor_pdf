import streamlit as st
import my_functions as mf


st.title("AutoPDF !")

pdfs_list = st.file_uploader(
    "Arraste os PDFs", type=["pdf"], accept_multiple_files=True
)


def run_app(pdfs_list):
    pdfs_names_list, pdfs_text_list = mf.read_pdfs(pdfs_list)

    st.success(f"Parabens, vc colocou {len(pdfs_list)} arquivos PDF !")

    list_pdf_answers = []
    for pdf_text in pdfs_text_list:
        topic_list = mf.split_into_topics(pdf_text)

        pdf_answers = []

        pdf_answers.extend(mf.get_topic_3_answers(topic_list[3]))
        pdf_answers.extend(mf.get_topic_4_answers(topic_list[4]))
        pdf_answers.extend(mf.get_topic_5_answers(topic_list[5]))

        list_pdf_answers.append(mf.create_answers_df(pdf_answers))

    df_preview = mf.create_preview(list_pdf_answers, pdfs_names_list)
    excel_sap = mf.create_sap_excel(list_pdf_answers)

    st.divider()
    st.download_button("Baixar Excel SAP", data=excel_sap, file_name="Excel_Isa.xlsx")

    st.divider()
    st.header("Prévia:")
    st.write(df_preview)


if len(pdfs_list) == 0:
    st.warning("Insira seus PDFs")
else:
    run_app(pdfs_list)
