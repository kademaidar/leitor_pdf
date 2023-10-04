import streamlit as st
import reader_functions as read
import writer_functions as write


def run_app(pdfs_list):
    st.success(f"Parabens, vc colocou {len(pdfs_list)} arquivos PDF !")

    list_pdf_answers = []
    list_pdf_names = []

    for pdf in pdfs_list:
        name, pdf_text = read.read_pdf(pdf)

        topic_list = read.split_into_topics(pdf_text)

        pdf_answers = []

        pdf_answers.extend(read.get_topic_3_answers(topic_list[3]))
        pdf_answers.extend(read.get_topic_4_answers(topic_list[4]))
        pdf_answers.extend(read.get_topic_5_answers(topic_list[5]))

        list_pdf_names.append(name)
        list_pdf_answers.append(write.create_answers_df(pdf_answers))

    df_preview = write.create_preview(list_pdf_names, list_pdf_answers)
    excel_sap = write.create_sap_excel(list_pdf_answers)

    st.divider()
    st.download_button("Baixar Excel SAP", data=excel_sap, file_name="Excel_Isa.xlsx")

    st.divider()
    st.header("Prévia:")
    st.write(df_preview)


st.title("AutoPDF !")

pdfs_list = st.file_uploader(
    "Arraste os PDFs", type=["pdf"], accept_multiple_files=True
)

if len(pdfs_list) == 0:
    st.warning("Insira seus PDFs")
else:
    run_app(pdfs_list)
