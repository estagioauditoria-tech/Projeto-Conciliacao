# test_end_to_end.py
# Teste completo do fluxo: Importação → Processamento → Geração

import sys
import os
import pandas as pd

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from conciliador.services.file_handler import read_file, write_file
from conciliador.services.sheet_processor import clean_sheet
from conciliador.services.data_mapper import extract_transactions
from conciliador.services.output_generator import gerar_planilha
from conciliador.models.template import Template

print("=" * 80)
print("TESTE END-TO-END COMPLETO - PIPELINE INTEIRO")
print("=" * 80)

# ===== PASSO 1: Criar planilha de teste (simula planilha real) =====
print("\n[1/6] Criando planilha de teste...")

# Simular uma planilha bagunçada (como vem de um banco)
dados_teste = {
    "Coluna1": [None, None, "ID", "001"],  # Coluna extra
    "Data Lançamento": [None, None, "Data do Pagamento", "06/10/2025"],
    "Forma Pagamento": [None, None, "Tipo", "pix"],
    "Valor Total": [None, None, "Quantia", 150.50],
    "Cliente": [None, None, "Nome", "João Silva"],
    "Unnamed: 1": [None, None, None, None]  # Coluna vazia
}

df_teste = pd.DataFrame(dados_teste)
arquivo_entrada = "planilha_teste_entrada.xlsx"
arquivo_saida = "planilha_teste_saida.xlsx"
write_file(df_teste, arquivo_entrada)
print(f"[OK] Planilha de teste criada: {arquivo_entrada}")

try:
    # ===== PASSO 2: Importar planilha =====
    print("\n[2/6] Importando planilha...")
    df = read_file(arquivo_entrada)
    print(f"[OK] Planilha importada: {df.shape[0]} linhas x {df.shape[1]} colunas")
    print(f"   Primeiras linhas:\n{df.head()}")

    # ===== PASSO 3: Limpar planilha =====
    print("\n[3/6] Limpando planilha...")
    df_limpo = clean_sheet(df)
    print(f"[OK] Planilha limpa: {df_limpo.shape[0]} linhas x {df_limpo.shape[1]} colunas")
    print(f"   Colunas: {list(df_limpo.columns)}")
    print(f"   Dados:\n{df_limpo}")

    # ===== PASSO 4: Extrair transactions =====
    print("\n[4/6] Extraindo transactions...")
    transactions, erros = extract_transactions(df_limpo)
    print(f"[OK] Transactions extraidas: {len(transactions)} sucesso, {len(erros)} erros")

    if transactions:
        print(f"   Primeira transaction:")
        t = transactions[0]
        print(f"      - Data: {t.data}")
        print(f"      - Valor: {t.valor}")
        print(f"      - Tipo: {t.tipo_pagamento}")
        print(f"      - Extras: {t.extras}")

    if erros:
        print(f"   Erros encontrados:")
        for erro in erros:
            print(f"      - {erro}")

    # ===== PASSO 5: Criar template de saída =====
    print("\n[5/6] Criando template de saída...")
    template_omie = Template(
        nome="Omie",
        colunas=["Data", "Valor", "Tipo de Pagamento", "Cliente"],
        mapeamento={
            "Data": "data",
            "Valor": "valor",
            "Tipo de Pagamento": "tipo_pagamento",
            "Cliente": "Nome"  # Campo extra (usa "Nome" da planilha)
        }
    )
    print(f"[OK] Template criado: {template_omie.nome}")
    print(f"   Colunas: {template_omie.colunas}")

    # ===== PASSO 6: Gerar planilha formatada =====
    print("\n[6/6] Gerando planilha formatada...")
    caminho_gerado = gerar_planilha(transactions, template_omie, arquivo_saida)
    print(f"[OK] Planilha gerada: {caminho_gerado}")

    # Verificar resultado final
    print("\n[VERIFICAÇÃO] Lendo planilha gerada...")
    df_resultado = pd.read_excel(arquivo_saida)
    print(f"[OK] Planilha final: {df_resultado.shape[0]} linhas x {df_resultado.shape[1]} colunas")
    print(f"   Colunas: {list(df_resultado.columns)}")
    print(f"   Dados:\n{df_resultado}")

    # Validar conteúdo
    print("\n[VALIDAÇÃO] Verificando valores...")
    validacao_ok = True

    if df_resultado.iloc[0]["Data"] != "06/10/2025":
        print(f"[ERRO] Data incorreta: {df_resultado.iloc[0]['Data']}")
        validacao_ok = False
    else:
        print(f"[OK] Data correta: {df_resultado.iloc[0]['Data']}")

    if df_resultado.iloc[0]["Valor"] != 150.50:
        print(f"[ERRO] Valor incorreto: {df_resultado.iloc[0]['Valor']}")
        validacao_ok = False
    else:
        print(f"[OK] Valor correto: {df_resultado.iloc[0]['Valor']}")

    if df_resultado.iloc[0]["Tipo de Pagamento"] != "pix":
        print(f"[ERRO] Tipo incorreto: {df_resultado.iloc[0]['Tipo de Pagamento']}")
        validacao_ok = False
    else:
        print(f"[OK] Tipo correto: {df_resultado.iloc[0]['Tipo de Pagamento']}")

    if df_resultado.iloc[0]["Cliente"] != "João Silva":
        print(f"[ERRO] Cliente incorreto: {df_resultado.iloc[0]['Cliente']}")
        validacao_ok = False
    else:
        print(f"[OK] Cliente correto: {df_resultado.iloc[0]['Cliente']}")

    # Resultado final
    print("\n" + "=" * 80)
    if validacao_ok:
        print("[SUCESSO] TESTE END-TO-END PASSOU COM SUCESSO!")
        print("Pipeline completo funcionando:")
        print("  Planilha bagunçada -> Limpeza -> Extracao -> Formatacao -> Excel final")
    else:
        print("[FALHA] TESTE END-TO-END FALHOU!")
    print("=" * 80)

except Exception as e:
    print(f"\n[ERRO CRITICO] ERRO NO PIPELINE: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Limpar arquivos de teste
    print("\n[LIMPEZA] Removendo arquivos de teste...")
    if os.path.exists(arquivo_entrada):
        os.remove(arquivo_entrada)
        print(f"[OK] Removido: {arquivo_entrada}")
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)
        print(f"[OK] Removido: {arquivo_saida}")

print("\n=== Teste end-to-end concluído ===")
