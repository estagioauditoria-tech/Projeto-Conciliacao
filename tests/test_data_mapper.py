"""
Testes para DataMapper
Autor: Paulo Ygor - Estagiário | Grupo Doma
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.conciliador.services.file_handler import read_file
from src.conciliador.services.sheet_processor import clean_sheet
from src.conciliador.services.data_mapper import column_identifier, extract_transactions


def test_data_mapper_completo():
    """
    Teste completo: FileHandler + SheetProcessor + DataMapper
    """
    print("=" * 80)
    print("TESTE COMPLETO: FileHandler + SheetProcessor + DataMapper")
    print("=" * 80)

    caminho = r"C:\Users\usuario\Downloads\x.xlsx"

    try:
        # 1. Ler arquivo
        print("\n[1/3] Lendo arquivo...")
        df_bruto = read_file(caminho)
        print(f"    Lido: {df_bruto.shape[0]} linhas x {df_bruto.shape[1]} colunas")

        # 2. Limpar planilha
        print("\n[2/3] Limpando planilha...")
        df_limpo = clean_sheet(df_bruto)
        print(f"    Limpo: {df_limpo.shape[0]} linhas x {df_limpo.shape[1]} colunas")
        print(f"    Colunas: {list(df_limpo.columns)}")

        # 3. Testar identificação de colunas
        print("\n[3/3] Identificando colunas...")
        mapeamento = column_identifier(df_limpo)
        print(f"    Mapeamento encontrado:")
        for campo, coluna in mapeamento.items():
            print(f"      {campo} -> {coluna}")

        # 4. Extrair transactions
        print("\n[4/4] Extraindo transactions...")
        sucessos, erros = extract_transactions(df_limpo)

        print(f"\n    Sucessos: {len(sucessos)} transactions criadas")
        print(f"    Erros: {len(erros)} linhas com erro")

        if sucessos:
            print(f"\n    Primeira transaction:")
            t = sucessos[0]
            print(f"      Data: {t.data}")
            print(f"      Valor: {t.valor}")
            print(f"      Tipo: {t.tipo_pagamento}")
            print(f"      Extras: {t.extras}")

        if erros:
            print(f"\n    Primeiros 5 erros:")
            for erro in erros[:5]:
                print(f"      - {erro}")

        # Resumo
        print("\n" + "=" * 80)
        print("RESUMO:")
        print("=" * 80)
        print(f"Total de linhas processadas: {df_limpo.shape[0]}")
        print(f"Transactions criadas: {len(sucessos)}")
        print(f"Erros encontrados: {len(erros)}")
        print(f"Taxa de sucesso: {len(sucessos)/df_limpo.shape[0]*100:.1f}%")

        return sucessos, erros

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    print("\nINICIANDO TESTES DO DATA_MAPPER\n")

    sucessos, erros = test_data_mapper_completo()

    print("\n" + "=" * 80)
    print("TESTES CONCLUIDOS")
    print("=" * 80)
