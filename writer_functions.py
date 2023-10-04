import io
import pandas as pd
import streamlit as st


def create_answers_df(pdf_answers):
    "Cria um df com as respostas de um unico pdf"

    header = [
        "Origem (Unidade)",
        "Mercadoria",
        "Moeda",
        "Valor Transportado",
        "Transportadora",
        "nº Aviso Seguradora",
        "Data do Aviso",
        "Tipo de Sinistro",
        "Data da Ocorrencia",
    ]

    if pdf_answers[2] == "USD":
        header.append("Valor Reclamado (USD)")
        last_column = "Valor Reclamado (BRL)"
    elif pdf_answers[2] == "BRL":
        header.append("Valor Reclamado (BRL)")
        last_column = "Valor Reclamado (USD)"

    df = pd.DataFrame([pdf_answers])
    df.columns = header
    df[last_column] = ["-"]

    return df


def create_preview(list_pdf_names, list_pdf_answers):
    "Junta os df das respostas"

    df = pd.concat(list_pdf_answers, ignore_index=True).T
    df.columns = list_pdf_names

    return df


def create_sap_excel(list_pdf_answers):
    "Recebe a lista de respostas da lista de pdfs, adiciona colunas, organiza a ordem das colunas, transforma em excel e retorna esse arquivo.xlsx"

    df = pd.concat(list_pdf_answers, ignore_index=True)  # Cria um df com as respostas

    df[  # Adiciona colunas faltantes e preenche com os valores
        [
            "Empresa",
            "Ramo",
            "Numero do Sinistro Seguradora",
            "Seguradora",
            "Corretora",
            "Status Processo (Geral)",
            "Apólice",
            "nº MDS",
            "Data do Encerramento",
            "Franquia (USD)",
            "Franquia (BRL)",
            "Valor Indenizado (USD)",
            "Valor Indenizado (BRL)",
            "taxa câmbio",
            "Valor Pendente (USD)",
            "Status Processo (Geral)",
        ]
    ] = [  # Preenche com os valores
        "CSPC",
        "Outros",
        "Carga Digital Isabelle",
        "AKAD",
        "MDS",
        "PENDENTE",
        " ",
        " ",
        " ",
        " ",
        "5000",
        " ",
        " ",
        " ",
        " ",
        "PENDENTE",
    ]

    df = df[  # Ordena as colunas do df final
        [
            "Empresa",
            "Ramo",
            "Apólice",
            "Numero do Sinistro Seguradora",
            "Seguradora",
            "nº Aviso Seguradora",
            "Corretora",
            "nº MDS",
            "Data da Ocorrencia",
            "Data do Aviso",
            "Data do Encerramento",
            "Origem (Unidade)",
            "Moeda",
            "Valor Transportado",
            "Valor Reclamado (USD)",
            "Valor Reclamado (BRL)",
            "Franquia (USD)",
            "Franquia (BRL)",
            "Valor Indenizado (USD)",
            "Valor Indenizado (BRL)",
            "taxa câmbio",
            "Valor Pendente (USD)",
            "Status Processo (Geral)",
            "Tipo de Sinistro",
            "Transportadora",
            "Mercadoria",
        ]
    ]

    st.write(df)

    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Aba_Isa")
    excel_file.seek(0)

    return excel_file


# def create_df(answers_list):
#     "Cria um df com as respostas"

#     header_excel = [
#         "Empresa",
#         "Ramo",
#         "Apólice",
#         "Numero do Sinistro Seguradora",
#         "Seguradora",
#         "nº Aviso Seguradora",
#         "Corretora",
#         "nº MDS",
#         "Data da Ocorrencia",
#         "Data do Aviso",
#         "Data do Encerramento",
#         "Origem (Unidade)",
#         "Moeda",
#         "Valor Transportado",
#         "Valor Reclamado (USD)",
#         "Valor Reclamado (BRL)",
#         "Franquia (USD)",
#         "Franquia (BRL)",
#         "Valor Indenizado (USD)",
#         "Valor Indenizado (BRL)",
#         "taxa câmbio",
#         "Valor Pendente (USD)",
#         "Status Processo (Geral)",
#         "Tipo de Sinistro",
#         "Transportadora",
#         "?? Mercadoria",
#     ]

#     standard = [
#         "??CSPC",
#         "??Outros",
#         "??27982022010621000000",
#         "??Carga Manual ECT2",
#         "??AKAD",
#         "x",  # 5 aviso_n
#         "??MDS",
#         "??",
#         "x",  # 8 data
#         "x",  # 9 data_vistoria
#         "??",
#         "x",  # 11 origem
#         "x",  # 12 currency
#         "x",  # 13 valor_embarcado
#         "x",  # 14 estimativa_prejuizo, se USD
#         "x",  # 15 estimativa_prejuizo, se BRL
#         "??",
#         "??R$ 5.000,00",
#         "??",
#         "??R$ -",
#         "??R$ -  ",
#         "??R$ -",
#         "??PENDENTE",
#         "x",  # 23 evento
#         "x",  # 24 transportadora
#         "x",  # 25 mercadoria
#     ]

#     list_index = [11, 15, 12, 13, 24, 5, 9, 23, 8, 14]

#     for i in range(len(list_index)):
#         # if list_index[i] == 12:
#         #     st.write(answers_list[i])
#         #     if answers_list[i] == "US$":
#         #         st.write("dolar")
#         #     elif answers_list[i] == "R$":
#         #         st.write("real")

#         standard[list_index[i]] = answers_list[i]

#     df = pd.DataFrame([header, standard])

#     st.write(answers_list)

#     # st.write(f"Confira os valores:")
#     st.write(df.T)
