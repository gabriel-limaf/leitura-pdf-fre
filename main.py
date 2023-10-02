import PyPDF2
import csv


def buscar_palavra_chave(pdf_path, palavra_chave):
    try:
        # Abre o arquivo PDF em modo de leitura binária
        with open(pdf_path, 'rb') as pdf_file:
            # Cria um objeto PDFReader
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Loop através de todas as páginas do PDF
            for pagina in range(len(pdf_reader.pages)):
                # Extrai o texto da página atual
                texto_pagina = pdf_reader.pages[pagina].extract_text().lower()

                # Verifica se a palavra-chave está no texto da página
                for palavra in palavra_chave:
                    if palavra in texto_pagina:
                        return True

            # Se a palavra-chave não for encontrada em nenhuma página
            return False

    except FileNotFoundError:
        print(f"O arquivo PDF '{pdf_path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")
    return False


# Exemplo de uso:
new_csv = []
palavra_chave = ['incentivo de longo prazo', 'stock options', 'phantom shares', 'ações restritas', 'matching']
with open('Empresas Listadas B3 - Leitura_FRE.csv', 'r', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.reader(arquivo_csv)
    next(leitor_csv, None)
    for linha in leitor_csv:
        pdf_path = linha[5]
        encontrado = buscar_palavra_chave(pdf_path, palavra_chave)
        if encontrado:
            status = 'Possui ILP'
            linha[7] = status
            new_csv.append(linha)
        else:
            status = 'NÃO Possui ILP'
            linha[7] = status
            new_csv.append(linha)

with open("results.csv", "w", newline="", encoding="utf-8") as arquivo_csv:
    escritor_csv = csv.writer(arquivo_csv, delimiter=",")
    cabecalho = [
                 'Razão Social',
                 'Nome de Pregão',
                 'Segmento',
                 'Código',
                 'Status FRE',
                 'File_Path',
                 'Segmento_B3',
                 'Status ILP'
    ]
    escritor_csv.writerow(cabecalho)
    for linha in new_csv:
        escritor_csv.writerow(linha)
