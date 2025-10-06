# Importações
import pandas as pd

#-----------Funções de Processamento de Planilhas-----------#
'''
Aqui serão definidas as funções para:
- Identificar cabeçalhos -> header_finder
- Remover vazios -> remove_empty
- Desmesclar células -> unmerge_cells
- Limpar planilhas -> clean_sheet
'''

def header_finder(df):
    # Lógica para identificar cabeçalhos
    '''
Vai iterar pelas linhas do DataFrame e identificar a linha que contém os cabeçalhos
com base em: 
Se a linha possui mais de 70% de células preenchidas, e ela possui mais de 70% de células que não sejam NaN, 
ela é considerada o cabeçalho.
    '''
    if not any("Unnamed" in str(col) for col in df.columns):  # Se não houver NaNs, cancela a busca
        return -1
    
    for i in range (len(df)):
        line = df.iloc[i]
        filled_cells = line.notna().sum()
        total_cells = len(line)
        if filled_cells / total_cells >= 0.7:
            return i

    return 0

def remove_empty(df):
    # Lógica para remover linhas/colunas vazias
    '''
Vai ler e identificar linhas e colunas que estão completamente vazias (NaN) e removê-las do DataFrame.
    '''
    df = df.dropna(how='all')  
    df = df.dropna(axis=1, how='all')

    return df

def unmerge_cells(df):
    # Lógica para desmesclar células
    '''
Preenche células mescladas com o valor da célula mais próxima acima.
    '''
    df = df.ffill(limit=10)  # Preenche valores NaN com o valor mais próximo
    return df

def clean_sheet(df):
    # Orquestra as funções de limpeza
    '''
Esta função chama as demais funções de limpeza em sequência para preparar a planilha para análise.
    1 - Coloca o header na posição correta
    2 - Remove linhas e colunas vazias
    3 - Desmescla células
    '''
    header_index = header_finder(df)

    # Só redefine cabeçalho se encontrou um (header_index >= 0)
    if header_index >= 0:
        df.columns = df.iloc[header_index]  # Define a linha do cabeçalho
        df = df[header_index + 1:]  # Remove linhas acima do cabeçalho

    df = remove_empty(df)  # Remove linhas e colunas vazias
    df = unmerge_cells(df)  # Desmescla células
    df = df.reset_index(drop=True)  # Reseta o índice
    return df


