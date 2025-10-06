# Importações
import pandas as pd 
from ..models.template import Template
from .file_handler import write_file

# Função para gerar saída
def gerar_planilha(transactions, template, output_path):
    '''
    Gera um arquivo de saída baseado em transações e um template.

    Parâmetros:
    - transactions: list[Transaction] - Lista de transações processadas
    - template: Template - Instância da classe Template (formato de saída)
    - output_path: str - Caminho onde o arquivo será salvo (deve terminar com .xlsx)

    Retorna:
    - str: Caminho do arquivo gerado
    '''
    # Validações 

    # Valida template
    if not isinstance(template, Template):
        raise ValueError("O template deve ser uma instância da classe Template.")

    # Valida transactions
    if len(transactions) == 0:
        raise ValueError("A lista de transações está vazia.")
    
    # Valida output_path
    if not isinstance(output_path, str):
        raise ValueError("O caminho de saída deve ser uma string.")
    if not output_path.strip():
        raise ValueError("O caminho de saída não pode ser vazio.")
    if not output_path.endswith('.xlsx'):
        raise ValueError("O arquivo de saída deve ser xlsx.")

    # Processamento

    # Cria lista para armazenar linhas
    linhas = []

    # Preenche lista com dados das transactions
    for transaction in transactions:
        linha = {}
        for coluna in template.colunas:
            valor = template.get_valor_mapeado(transaction, coluna)
            linha[coluna] = valor
        linhas.append(linha)

    # Cria DataFrame de uma vez com todas as linhas
    df = pd.DataFrame(linhas, columns=template.colunas)

    # Salva com write_file
    write_file(df, output_path)

    # Retorna o caminho do arquivo gerado
    return output_path
