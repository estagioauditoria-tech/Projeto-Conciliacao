"""
Testes para FileHandler
Autor: Paulo Ygor - Estagiário | Grupo Doma
"""

import sys
import os

# Adiciona o diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.conciliador.services.file_handler import read_file, write_file


def test_read_planilha_real():
    """
    Teste 1: Ler planilha real do projeto
    """
    print("=" * 80)
    print("TESTE 1: Lendo planilha real (Historico Operacional)")
    print("=" * 80)

    caminho = r"C:\Users\usuario\Downloads\x.xlsx"

    try:
        # Ler arquivo
        df = read_file(caminho)

        # Mostrar informações
        print(f"\nArquivo lido com sucesso!")
        print(f"Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas")
        print(f"\nColunas encontradas:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i}. {col}")

        print(f"\nPrimeiras 5 linhas:")
        print(df.head())

        print(f"\nTipos de dados:")
        print(df.dtypes)

        print(f"\nInformacoes gerais:")
        print(df.info())

        return df

    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return None
    except ValueError as e:
        print(f"Erro: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None


def test_write_planilha():
    """
    Teste 2: Escrever DataFrame em arquivo Excel
    """
    print("\n" + "=" * 80)
    print("TESTE 2: Escrevendo DataFrame de teste")
    print("=" * 80)

    import pandas as pd

    # Criar DataFrame de teste
    df_teste = pd.DataFrame({
        'Data': ['01/10/2025', '02/10/2025', '03/10/2025'],
        'Valor': [150.50, 200.00, 75.25],
        'Tipo': ['PIX', 'Cartão', 'Dinheiro']
    })

    caminho_saida = "tests/output_teste.xlsx"

    try:
        write_file(df_teste, caminho_saida)
        print(f"Arquivo salvo com sucesso em: {caminho_saida}")

        # Tentar ler de volta para validar
        df_lido = read_file(caminho_saida)
        print(f"Arquivo re-lido com sucesso!")
        print(f"Dimensoes: {df_lido.shape[0]} linhas x {df_lido.shape[1]} colunas")
        print(f"\nConteudo:")
        print(df_lido)

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    print("\nINICIANDO TESTES DO FILE_HANDLER\n")

    # Teste 1: Ler planilha real
    df = test_read_planilha_real()

    # Teste 2: Escrever planilha
    test_write_planilha()

    print("\n" + "=" * 80)
    print("TESTES CONCLUIDOS")
    print("=" * 80)
