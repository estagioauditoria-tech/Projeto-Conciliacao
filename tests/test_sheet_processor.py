"""
Testes para SheetProcessor
Autor: Paulo Ygor - Estagiário | Grupo Doma
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.conciliador.services.file_handler import read_file
from src.conciliador.services.sheet_processor import clean_sheet, header_finder, remove_empty, unmerge_cells


def test_sheet_processor_completo():
    """
    Teste completo: FileHandler + SheetProcessor
    """
    print("=" * 80)
    print("TESTE COMPLETO: FileHandler + SheetProcessor")
    print("=" * 80)

    caminho = r"C:\Users\usuario\Downloads\x.xlsx"

    try:
        # 1. Ler arquivo (FileHandler)
        print("\n[1/2] Lendo arquivo com FileHandler...")
        df_bruto = read_file(caminho)
        print(f"    Dimensoes BRUTAS: {df_bruto.shape[0]} linhas x {df_bruto.shape[1]} colunas")
        print(f"    Colunas BRUTAS (primeiras 5): {list(df_bruto.columns[:5])}")
        print(f"\n    Primeiras 3 linhas BRUTAS:")
        print(df_bruto.head(3))

        # 2. Limpar planilha (SheetProcessor)
        print("\n[2/2] Limpando planilha com SheetProcessor...")
        df_limpo = clean_sheet(df_bruto)
        print(f"    Dimensoes LIMPAS: {df_limpo.shape[0]} linhas x {df_limpo.shape[1]} colunas")
        print(f"    Colunas LIMPAS (primeiras 10):")
        for i, col in enumerate(list(df_limpo.columns[:10]), 1):
            print(f"        {i}. {col}")

        print(f"\n    Primeiras 5 linhas LIMPAS:")
        print(df_limpo.head(5))

        print(f"\n    Tipos de dados:")
        print(df_limpo.dtypes)

        print(f"\n    Valores NaN restantes por coluna (primeiras 10):")
        nan_count = df_limpo.isna().sum()
        print(nan_count.head(10))

        # 3. Comparação Antes x Depois
        print("\n" + "=" * 80)
        print("RESUMO DA LIMPEZA:")
        print("=" * 80)
        print(f"Linhas removidas: {df_bruto.shape[0] - df_limpo.shape[0]}")
        print(f"Colunas removidas: {df_bruto.shape[1] - df_limpo.shape[1]}")
        print(f"\nAntes:  {df_bruto.shape[0]} linhas x {df_bruto.shape[1]} colunas")
        print(f"Depois: {df_limpo.shape[0]} linhas x {df_limpo.shape[1]} colunas")

        return df_limpo

    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_funcoes_individuais():
    """
    Teste individual de cada função do SheetProcessor
    """
    print("\n" + "=" * 80)
    print("TESTE INDIVIDUAL: Funções do SheetProcessor")
    print("=" * 80)

    caminho = r"C:/Users/usuario/Downloads/x.xlsx"

    try:
        df = read_file(caminho)

        # Teste 1: header_finder
        print("\n[Teste 1] header_finder()")
        header_index = header_finder(df)
        print(f"    Indice do cabecalho: {header_index}")
        print(f"    Conteudo da linha {header_index}:")
        print(f"    {list(df.iloc[header_index][:10])}")

        # Teste 2: remove_empty
        print("\n[Teste 2] remove_empty()")
        df_sem_vazios = remove_empty(df)
        print(f"    Antes:  {df.shape}")
        print(f"    Depois: {df_sem_vazios.shape}")

        # Teste 3: unmerge_cells
        print("\n[Teste 3] unmerge_cells()")
        nan_antes = df_sem_vazios.isna().sum().sum()
        df_desmesclado = unmerge_cells(df_sem_vazios)
        nan_depois = df_desmesclado.isna().sum().sum()
        print(f"    NaN antes:  {nan_antes}")
        print(f"    NaN depois: {nan_depois}")
        print(f"    NaN removidos: {nan_antes - nan_depois}")

    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n INICIANDO TESTES DO SHEET_PROCESSOR\n")

    # Teste completo
    df_limpo = test_sheet_processor_completo()

    # Testes individuais
    test_funcoes_individuais()

    print("\n" + "=" * 80)
    print("TESTES CONCLUIDOS")
    print("=" * 80)
