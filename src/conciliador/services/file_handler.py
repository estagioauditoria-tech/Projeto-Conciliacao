# Importações 
import pandas as pd
import os

#----------Função para ler um arquivo Excel e retornar um DataFrame-------------

def read_file(file_path):
    ''' 
    Lê um arquivo Excel e retorna um DataFrame do pandas.
    Suporta arquivos com extensões .xls, .xlsx.
    '''
    # Verifica se o arquivo existe e se a extensão é válida
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
    if not file_path.endswith(('.xls', '.xlsx')):
        raise ValueError("O arquivo deve ter extensão .xls ou .xlsx.")

    # Lê o arquivo Excel usando engine apropriado
    try:
        df = pd.read_excel(file_path, engine='openpyxl' if file_path.endswith('.xlsx') else 'xlrd')
    except Exception as e:
        raise IOError(f"Erro ao ler o arquivo: {e}")

    return df

#----------Função para escrever um DataFrame em um arquivo Excel-------------

def write_file(df, file_path):
    ''' 
    Escreve um DataFrame do pandas em um arquivo Excel.
    Suporta arquivos com extensões .xls, .xlsx.
    '''
    # Verifica conteúdo do DataFrame
    if df is None:
        raise ValueError("O DataFrame é None e não pode ser salvo.")
    if df.empty:
        raise ValueError("O DataFrame está vazio e não pode ser salvo.")

    # Transforma o DataFrame em um arquivo Excel
    try:
        df.to_excel(file_path)
    except Exception as e:
        raise IOError(f"Erro ao salvar o arquivo: {e}")
    return True
