import pandas as pd
import PyPDF2
import io
import re
import streamlit as st


def read_pdfs(pdfs_list):
    "Recebe uma lista de arquivos pdf no formato binario e retorna uma lista de strings com os textos"

    text_content_list = []
    names_list = []
    for pdf_file in pdfs_list:
        names_list.append(pdf_file.name)

        pdf_data = PyPDF2.PdfReader(pdf_file)
        text_content_list.append(pdf_data.pages[0].extract_text())

    return names_list, text_content_list


def split_into_topics(text_content):
    "Recebe um pdf, separa cada topico, retorna uma lista com o texto de cada topico"

    lines_list = text_content.split("\n")

    index_list = []
    topics_list = []

    key_words_list = [
        "RELATÓRIO PRELIMINAR - VIA DO CORRETOR/SEGURADO",
        "1-REGULADORA",
        "2-SEGURADO",
        "3-EMBARQUE",
        "4-COMUNICAÇÃO DO SINISTRO",
        "5-SINISTRO",
        "8-SALVADOS",
    ]

    for key_word in key_words_list:
        index_list.append(lines_list.index(key_word))

    for i in range(len(key_words_list)):
        if i < len(key_words_list) - 1:
            topics_list.append(lines_list[index_list[i] : index_list[i + 1]])
        else:
            topics_list.append(lines_list[index_list[i] :])

    return topics_list


def get_topic_3_answers(topic_3):
    "Recebe as linhas do topico '3-EMBARQUE' e retorna uma lista com os valores procurados"

    # Search for the ORIGEM answer
    origem_line = topic_3[2]
    city_regex = r"\b[a-zA-ZÀ-ÖØ-öø-ÿ\s]+/[A-Z]{2}\b"
    cities_list = re.findall(city_regex, origem_line)
    origem = cities_list[0][
        1:
    ]  # The city name was coming with whitespace at the beginning

    # Search for VALOR TOTAL EMBARCADO answer
    mercadoria_line = topic_3[8].replace(".", "")
    money_regex = r"(?:US\$|R\$)\s\d+,\d{2}"
    re_return = re.search(money_regex, mercadoria_line)
    str_valor_embarcado = re_return.group()

    if str_valor_embarcado.split()[0] == "US$":
        currency = "USD"
    elif str_valor_embarcado.split()[0] == "R$":
        currency = "BRL"
    else:
        currency = "outro"

    valor_embarcado = float(str_valor_embarcado.split()[1].replace(",", "."))

    # Search for the MERCADORIA(S) answer
    mercadoria = mercadoria_line[0 : re_return.start()]

    # Search for the TRANSPORTADORA answer
    transportadora = topic_3[10]

    return [origem, mercadoria, currency, valor_embarcado, transportadora]


def get_topic_4_answers(topic_4):
    "Recebe as linhas do topico '4-COMUNICAÇÃO...' e retorna uma lista com os valores procurados"

    # Search for the AVISO N answer
    aviso_n = topic_4[2]

    # Search for the DATA DA VISTORIA answer
    if len(topic_4) > 4:
        data_vistoria = topic_4[4]
    else:
        data_vistoria = "(sem resposta)"  # ANTENCAO o que colocar nesse caso ?

    return [aviso_n, data_vistoria]


def get_topic_5_answers(topic_5):
    "Recebe as linhas do topico '5-SINISTRO' e retorna uma lista com os valores procurados"

    evento_line = topic_5[2]

    # Search for the DATA answer
    date_regex = r"\d{2}/\d{2}/\d{4}"
    re_return = re.search(date_regex, evento_line)
    data = re_return.group()

    # Search for the EVENTO answer
    evento = evento_line[0 : re_return.start()]

    # Search for the ESTIMATIVA... answer
    estimativa_prejuizo = float(
        topic_5[-1].split()[1].replace(".", "").replace(",", ".")
    )

    return [evento, data, estimativa_prejuizo]


def create_answers_df(pdf_answers):
    "Cria um df com as respostas de um unico pdf"

    header = [
        "Origem (Unidade)",
        "?? Mercadoria",
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


def create_preview(list_pdf_answers, pdfs_names_list):
    "Junta os df das respostas"

    df = pd.concat(list_pdf_answers, ignore_index=True).T
    df.columns = pdfs_names_list

    return df


def create_sap_excel(list_pdf_answers):
    "Usa o df_preview, adiciona algumas colunas e cria o excel para o SAP"

    df = pd.concat(list_pdf_answers, ignore_index=True)

    df[
        [
            "Empresa",
            "Ramo",
            "Numero do Sinistro Seguradora",
            "Seguradora",
            "Corretora",
            "Status Processo (Geral)",
        ]
    ] = ["CSPC", "Outros", "Carga Digital Isabelle", "AKAD", "MDS", "PENDENTE"]

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
