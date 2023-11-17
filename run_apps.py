import pandas as pd
import streamlit as st
import reader_functions as read
import writer_functions as write
from analyze_functions import analyze
import time


def pdf_app(pdfs_list):
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
    excel_pbi = write.create_pbi_excel(list_pdf_answers)

    st.subheader("", divider="rainbow")
    st.subheader(":blue[Prévia]")
    st.write(df_preview)

    st.subheader("", divider="rainbow")
    st.subheader(":red[Downloads]")
    # fmt: off
    col1, col2, _ = st.columns(3)
    # fmt: on
    with col1:
        st.download_button(
            "Excel SAP",
            data=excel_sap,
            file_name="excel_SAP_Isa.xlsx",
            help="Use essa tabela para fazer uma carga de varios Sinistros ao mesmo tempo",
            type="primary",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            "Excel PowerBI",
            data=excel_pbi,
            file_name="excel_PowerBI_Isa.xlsx",
            help="Use essa tabela para atualizar o Power BI",
            type="primary",
            use_container_width=True,
        )


def excel_app(excel_list):
    progress_bar = st.progress(0, "Analisando")
    time.sleep(0.5)
    progress_bar.progress(10, "Analisando")
    df_list = [pd.read_excel(excel) for excel in excel_list]  # Sempre 2 itens

    df0_columns = list(df_list[0].columns)
    df1_columns = list(df_list[1].columns)

    # fmt: off
    powerbi_columns= ["Linha de Seguro", "Ramo", "Status", "Nº Aviso Seguradora",
        "Data da Ocorrência","Data do Aviso","Data do Encerramento","nº MDS",
        "Tipo de Sinistro","Ocorrência","Unidade de Negócio","Carregamento",
        "Origem (Unidade)","Entrega (destino)","Mercadoria (Transportes)",
        "Modal de Transporte","Transportadora","Motorista","Placa","Valor Transportado (BRL)",
        "Valor Transportado (USD)","Valor Reclamado (BRL)","Valor Reclamado (USD)",
        "Franquia (BRL)","Franquia (USD)","Valor Indenizado (BRL)","Valor Indenizado (USD)",
        "Valor Pendente (BRL)","Valor Pendente (USD)"]

    embarque_columns = ["Centro", "Denominação", "Nº transporte", "Nrº NFe", 
        "Denominação.1", "Nome Transportadora", "Unidade de peso", "Peso líquido",
        "Peso total", "Placa Simples Veículo", "Capacidade Veículo", "Data Transporte",
        "Valor total incl.imp."]
    # fmt: on

    if df0_columns == powerbi_columns and df1_columns == embarque_columns:
        df_results = analyze(df_list[0], df_list[1])

    elif df0_columns == embarque_columns and df1_columns == powerbi_columns:
        df_results = analyze(df_list[1], df_list[0])

    else:
        st.warning("ERRO: Confira as tabelas enviadas")
        progress_bar.empty()
        return

    st.subheader("", divider="rainbow")
    st.subheader(":blue[Análise] das Transportadoras")
    st.write(df_results)
    st.caption(
        """Apresentamos todas as transportadoras que passaram por algum sinistro, 
        e a porcentagem dos valores transportados que foram sinistrados"""
    )
    progress_bar.progress(100, "Analisando")
    time.sleep(1)
    progress_bar.empty()
