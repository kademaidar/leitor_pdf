import PyPDF2


def read_pdf(arquivo_pdf):
    "Lê um arquivo pdf no formato binario e retorna uma string com o texto"

    pdf_data = PyPDF2.PdfReader(arquivo_pdf)
    page1 = pdf_data.pages[0]

    return page1.extract_text()
