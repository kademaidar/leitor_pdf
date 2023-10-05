import io
import pandas as pd
import streamlit as st


def create_answers_df(pdf_answers):
    "Recebe um pdf e cria um df com as respostas"

    df = pd.DataFrame([pdf_answers])

    header = [
        "Moeda",
        "Origem (Unidade)",
        "Entrega (destino)",
        "Mercadoria",
        "Valor Transportado",
        "Transportadora",
        "Motorista",
        "Placa",
        "nº Aviso Seguradora",
        "Data do Aviso",
        "Tipo de Sinistro",
        "Data da Ocorrencia",
    ]

    if pdf_answers[0] == "USD":
        header.append("Valor Reclamado (USD)")
        last_column = "Valor Reclamado (BRL)"

    elif pdf_answers[0] == "BRL":
        header.append("Valor Reclamado (BRL)")
        last_column = "Valor Reclamado (USD)"

    df.columns = header
    df[last_column] = " "

    if pdf_answers[0] == "USD":
        # Subtrai a franquia do valor reclamado levando em conta a moeda
        df["Valor Pendente (BRL)"] = " "
        df["Valor Pendente (USD)"] = round(
            max(df["Valor Reclamado (USD)"][0] - 20000, 0), 2
        )
        # Nome é diferente no SAP e no BI, porém o mesmo dado
        df["Valor Transportado (USD)"] = df["Valor Transportado"]
        df["Valor Transportado (BRL)"] = " "

    elif pdf_answers[0] == "BRL":
        df["Valor Pendente (USD)"] = " "
        df["Valor Pendente (BRL)"] = round(
            max(df["Valor Reclamado (BRL)"][0] - 5000, 0), 2
        )
        df["Valor Transportado (USD)"] = " "
        df["Valor Transportado (BRL)"] = df["Valor Transportado"]

    return df


def create_preview(list_pdf_names, list_pdf_answers):
    "Junta os df das respostas"

    df = pd.concat(list_pdf_answers, ignore_index=True).T
    df.columns = list_pdf_names

    return df


def create_sap_excel(list_pdf_answers):
    "Recebe a lista de respostas da lista de pdfs, adiciona colunas, organiza a ordem das colunas, transforma em excel e retorna esse arquivo.xlsx"

    df = pd.concat(list_pdf_answers, ignore_index=True)  # Cria um df com as respostas

    df[  # Adiciona as colunas que tem resposta fixa
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
    ] = [  # Preenche com as respostas fixas
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
        5000,
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

    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Aba_Isa")
    excel_file.seek(0)

    return excel_file


def create_pbi_excel(list_pdf_answers):
    "Recebe a lista de respostas da lista de pdfs, adiciona colunas, organiza a ordem das colunas, transforma em excel e retorna esse arquivo.xlsx"

    df = pd.concat(list_pdf_answers, ignore_index=True).rename(
        columns={
            "nº Aviso Seguradora": "Nº Aviso Seguradora",
            "Data da Ocorrencia": "Data da Ocorrência",
            "Mercadoria": "Mercadoria (Transportes)",
        }
    )

    df[  # Adiciona as colunas que tem resposta fixa
        [
            "Linha de Seguro",
            "Ramo",
            "Status",
            "Data do Encerramento",
            "nº MDS",
            "Unidade de Negócio",
            "Carregamento",
            "Modal de Transporte",
            "Franquia (BRL)",
            "Franquia (USD)",
            "Valor Indenizado (BRL)",
            "Valor Indenizado (USD)",
        ]
    ] = [  # Preenche com as respostas fixas
        "Transporte",
        " ",
        "Pendente",
        " ",
        " ",
        " ",
        " ",
        " ",
        5000,
        20000,
        " ",
        " ",
    ]

    df["Ocorrência"] = df["Tipo de Sinistro"]

    df = df[  # Ordena as colunas do df final, também filtra apenas as colunas desse excel
        [
            "Linha de Seguro",
            "Ramo",
            "Status",
            "Nº Aviso Seguradora",
            "Data da Ocorrência",
            "Data do Aviso",
            "Data do Encerramento",
            "nº MDS",
            "Tipo de Sinistro",
            "Ocorrência",
            "Unidade de Negócio",
            "Carregamento",
            "Origem (Unidade)",
            "Entrega (destino)",
            "Mercadoria (Transportes)",
            "Modal de Transporte",
            "Transportadora",
            "Motorista",
            "Placa",
            "Valor Transportado (BRL)",
            "Valor Transportado (USD)",
            "Valor Reclamado (BRL)",
            "Valor Reclamado (USD)",
            "Franquia (BRL)",
            "Franquia (USD)",
            "Valor Indenizado (BRL)",
            "Valor Indenizado (USD)",
            "Valor Pendente (BRL)",
            "Valor Pendente (USD)",
        ]
    ]

    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False, sheet_name="Aba_Isa")
    excel_file.seek(0)

    return excel_file
