# test_output_generator.py
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from conciliador.services.output_generator import gerar_planilha
from conciliador.models.template import Template
from conciliador.models.transaction import Transaction
import pandas as pd

# Teste 1: Gerar planilha com sucesso
print("=== Teste 1: Gerar planilha com sucesso ===")
try:
    # Criar transactions
    transactions = [
        Transaction(data="06/10/2025", valor=150.50, tipo_pagamento="pix", cliente="João Silva"),
        Transaction(data="07/10/2025", valor=200.00, tipo_pagamento="débito", cliente="Maria Santos"),
        Transaction(data="08/10/2025", valor=75.00, tipo_pagamento="dinheiro", cliente="Pedro Costa")
    ]

    # Criar template
    template = Template(
        nome="Teste",
        colunas=["Data", "Valor", "Tipo", "Cliente"],
        mapeamento={"Data": "data", "Valor": "valor", "Tipo": "tipo_pagamento", "Cliente": "cliente"}
    )

    # Gerar planilha
    caminho_saida = "test_output.xlsx"
    resultado = gerar_planilha(transactions, template, caminho_saida)

    print(f"✅ Planilha gerada em: {resultado}")

    # Verificar se arquivo foi criado
    if os.path.exists(caminho_saida):
        print("✅ Arquivo criado com sucesso!")

        # Ler arquivo para verificar conteúdo
        df_resultado = pd.read_excel(caminho_saida)
        print(f"✅ Planilha tem {len(df_resultado)} linhas e {len(df_resultado.columns)} colunas")
        print(f"   Colunas: {list(df_resultado.columns)}")
        print(f"   Primeira linha: {df_resultado.iloc[0].to_dict()}")

        # Limpar arquivo de teste
        os.remove(caminho_saida)
        print("✅ Arquivo de teste removido")
    else:
        print("❌ Arquivo não foi criado!")

except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 2: Validação - template inválido
print("\n=== Teste 2: Template inválido (deve dar erro) ===")
try:
    transactions = [Transaction(data="06/10/2025", valor=150.50, tipo_pagamento="PIX")]
    gerar_planilha(transactions, "não é template", "saida.xlsx")
    print("❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")
except TypeError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 3: Validação - lista vazia
print("\n=== Teste 3: Lista de transactions vazia (deve dar erro) ===")
try:
    template = Template(
        nome="Teste",
        colunas=["Data"],
        mapeamento={"Data": "data"}
    )
    gerar_planilha([], template, "saida.xlsx")
    print("❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 4: Validação - caminho inválido (sem .xlsx)
print("\n=== Teste 4: Caminho sem .xlsx (deve dar erro) ===")
try:
    transactions = [Transaction(data="06/10/2025", valor=150.50, tipo_pagamento="PIX")]
    template = Template(
        nome="Teste",
        colunas=["Data"],
        mapeamento={"Data": "data"}
    )
    gerar_planilha(transactions, template, "saida.csv")
    print("❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 5: Validação - caminho vazio
print("\n=== Teste 5: Caminho vazio (deve dar erro) ===")
try:
    transactions = [Transaction(data="06/10/2025", valor=150.50, tipo_pagamento="PIX")]
    template = Template(
        nome="Teste",
        colunas=["Data"],
        mapeamento={"Data": "data"}
    )
    gerar_planilha(transactions, template, "")
    print("❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 6: Verificar conteúdo correto da planilha
print("\n=== Teste 6: Verificar valores corretos na planilha ===")
try:
    transactions = [
        Transaction(data="06/10/2025", valor=150.50, tipo_pagamento="PIX")
    ]

    template = Template(
        nome="Teste",
        colunas=["Data", "Valor"],
        mapeamento={"Data": "data", "Valor": "valor"}
    )

    caminho_saida = "test_valores.xlsx"
    gerar_planilha(transactions, template, caminho_saida)

    # Ler e verificar
    df = pd.read_excel(caminho_saida)

    if df.iloc[0]["Data"] == "06/10/2025" and df.iloc[0]["Valor"] == 150.50:
        print("✅ Valores corretos na planilha!")
    else:
        print(f"❌ Valores incorretos: {df.iloc[0].to_dict()}")

    # Limpar
    os.remove(caminho_saida)

except Exception as e:
    print(f"❌ Erro: {e}")

print("\n=== Testes concluídos ===")
