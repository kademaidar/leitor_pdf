import PyPDF2
import re
import streamlit as st


def read_pdf(pdf):
    "Recebe um pdf no formato binario e retorna o nome e o texto"

    pdf_data = PyPDF2.PdfReader(pdf)
    pdf_text_page1 = pdf_data.pages[0].extract_text()
    pdf_text_page2 = pdf_data.pages[1].extract_text()

    pdf_text = pdf_text_page1 + " " + pdf_text_page2

    return pdf.name, pdf_text


def split_into_topics(text_content):
    "Recebe um pdf, separa cada topico, retorna uma lista com o texto de cada topico"

    lines_list = text_content.split("\n")

    index_list = []
    topics_list = []

    title_topics_list = [
        "RELATÓRIO PRELIMINAR - VIA DO CORRETOR/SEGURADO",
        "1-REGULADORA",
        "2-SEGURADO",
        "3-EMBARQUE",
        "4-COMUNICAÇÃO DO SINISTRO",
        "5-SINISTRO",
        "8-SALVADOS",
    ]

    for key_word in title_topics_list:
        index_list.append(lines_list.index(key_word))

    for i in range(len(title_topics_list)):
        if i < len(title_topics_list) - 1:
            topics_list.append(lines_list[index_list[i] : index_list[i + 1]])
        else:
            topics_list.append(lines_list[index_list[i] :])

    return topics_list


def get_topic_3_answers(topic_3):
    "Recebe as linhas do topico '3-EMBARQUE' e retorna uma lista com os valores procurados"

    # Search for the ORIGEM answer
    answers_line = topic_3[2]

    city_regex_slash = r"\b[a-zA-ZÀ-ÖØ-öø-ÿ\s]+/[A-Z]{2}\b"
    city_regex_hyphen = r"\b[A-Z][a-zA-ZÀ-ÖØ-öø-ÿ\s]+ - [A-Z]{2}\b"

    cities_list = re.findall(city_regex_slash, answers_line)
    if len(cities_list) == 0:
        cities_list = re.findall(city_regex_hyphen, answers_line)

    origem = cities_list[0].strip()  # Remove undesired whitespaces

    # Search for the DESTINO answer
    destino = cities_list[-1].strip()

    # Search for VALOR TOTAL EMBARCADO answer
    mercadoria_line = topic_3[8].replace(".", "")
    money_regex = r"(?:US\$|R\$)\s\d+,\d{2}"
    re_return = re.search(money_regex, mercadoria_line)
    str_valor_embarcado = re_return.group()

    if str_valor_embarcado.split()[0] == "US$":  # Look for currency value
        currency = "USD"
    elif str_valor_embarcado.split()[0] == "R$":
        currency = "BRL"
    else:
        currency = "outro"

    valor_transportado = float(str_valor_embarcado.split()[1].replace(",", "."))

    # Search for the MERCADORIA(S) answer
    mercadoria = mercadoria_line[0 : re_return.start()]

    # Search for the TRANSPORTADORA answer
    transportadora = topic_3[10]
    motorista_index = 12
    if transportadora == "MOTORISTA":  # Occours when TRANSPORTADORA dont have answer
        transportadora = " "
        motorista_index = 11

    # Search for MOTORISTA answer
    motorista = topic_3[motorista_index]

    # Search for PLACA 1 answer
    placa_index = motorista_index + 2
    placa_line = topic_3[placa_index]
    placa = placa_line[:8].strip()

    return [
        currency,
        origem,
        destino,
        mercadoria,
        valor_transportado,
        transportadora,
        motorista,
        placa,
    ]


def get_topic_4_answers(topic_4):
    "Recebe as linhas do topico '4-COMUNICAÇÃO...' e retorna uma lista com os valores procurados"

    # Search for the AVISO N answer
    aviso_n = topic_4[2]

    # Search for the DATA DA VISTORIA answer
    if len(topic_4) > 4:
        data_vistoria = topic_4[4]
    else:
        data_vistoria = " "  # ANTENCAO o que colocar nesse caso ?

    return [aviso_n, data_vistoria]


def get_topic_5_answers(topic_5):
    "Recebe as linhas do topico '5-SINISTRO' e retorna uma lista com os valores procurados"

    evento_line = topic_5[2]

    # Search for the DATA answer
    date_regex = r"\d{2}/\d{2}/\d{4}"
    re_return = re.search(date_regex, evento_line)
    data = re_return.group()

    # Search for the EVENTO answer
    evento = evento_line[0 : re_return.start()].strip()

    # Search for the ESTIMATIVA... answer
    estimativa_prejuizo = float(
        topic_5[-1].split()[1].replace(".", "").replace(",", ".")
    )

    return [evento, data, estimativa_prejuizo]
