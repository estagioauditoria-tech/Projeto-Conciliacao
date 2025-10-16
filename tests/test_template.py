# test_template.py
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from conciliador.models.template import Template

# Teste 1: Template válido
print("=== Teste 1: Template válido ===")
try:
    template = Template(
        nome="Omie",
        colunas=["Data", "Valor", "Tipo"],
        mapeamento={"Data": "data", "Valor": "valor", "Tipo": "tipo_pagamento"},
        formatacao={"cor_cabecalho": "#4472C4"}
    )
    print(f"✅ Template criado: {template.nome}")
    print(f"   Colunas: {template.colunas}")
    print(f"   Mapeamento: {template.mapeamento}")
    print(f"   Formatação: {template.formatacao}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 2: Template sem formatação (deve usar default)
print("\n=== Teste 2: Template sem formatação ===")
try:
    template = Template(
        nome="Simples",
        colunas=["Data", "Valor"],
        mapeamento={"Data": "data", "Valor": "valor"}
    )
    print(f"✅ Template criado: {template.nome}")
    print(f"   Formatação (default): {template.formatacao}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 3: Nome vazio (deve dar erro)
print("\n=== Teste 3: Nome vazio (deve dar erro) ===")
try:
    template = Template(
        nome="",
        colunas=["Data"],
        mapeamento={"Data": "data"}
    )
    print(f"❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 4: Colunas vazia (deve dar erro)
print("\n=== Teste 4: Colunas vazia (deve dar erro) ===")
try:
    template = Template(
        nome="Teste",
        colunas=[],
        mapeamento={}
    )
    print(f"❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 5: Mapeamento com chaves diferentes das colunas (deve dar erro)
print("\n=== Teste 5: Chaves do mapeamento diferentes (deve dar erro) ===")
try:
    template = Template(
        nome="Teste",
        colunas=["Data", "Valor"],
        mapeamento={"Data": "data", "Tipo": "tipo"}  # "Tipo" não está nas colunas
    )
    print(f"❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 6: Mapeamento faltando uma coluna (deve dar erro)
print("\n=== Teste 6: Mapeamento incompleto (deve dar erro) ===")
try:
    template = Template(
        nome="Teste",
        colunas=["Data", "Valor", "Tipo"],
        mapeamento={"Data": "data", "Valor": "valor"}  # Falta "Tipo"
    )
    print(f"❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 7: Colunas não são strings (deve dar erro)
print("\n=== Teste 7: Coluna não é string (deve dar erro) ===")
try:
    template = Template(
        nome="Teste",
        colunas=["Data", 123],  # 123 não é string
        mapeamento={"Data": "data", 123: "valor"}
    )
    print(f"❌ Não deveria ter funcionado!")
except TypeError as e:
    print(f"✅ Erro capturado: {e}")

# Teste 8: get_valor_mapeado() com campos obrigatórios
print("\n=== Teste 8: get_valor_mapeado() - campos obrigatórios ===")
try:
    from conciliador.models.transaction import Transaction

    transaction = Transaction(
        data="06/10/2025",
        valor=150.50,
        tipo_pagamento="PIX",
        cliente="João Silva"
    )

    template = Template(
        nome="Teste",
        colunas=["Data", "Valor", "Tipo"],
        mapeamento={"Data": "data", "Valor": "valor", "Tipo": "tipo_pagamento"}
    )

    valor_data = template.get_valor_mapeado(transaction, "Data")
    valor_valor = template.get_valor_mapeado(transaction, "Valor")
    valor_tipo = template.get_valor_mapeado(transaction, "Tipo")

    print(f"✅ Valores extraídos:")
    print(f"   Data: {valor_data}")
    print(f"   Valor: {valor_valor}")
    print(f"   Tipo: {valor_tipo}")

    if valor_data == "06/10/2025" and valor_valor == 150.50 and valor_tipo == "PIX":
        print("✅ Todos os valores corretos!")
    else:
        print("❌ Valores incorretos!")

except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 9: get_valor_mapeado() com campos extras
print("\n=== Teste 9: get_valor_mapeado() - campos extras ===")
try:
    transaction = Transaction(
        data="06/10/2025",
        valor=150.50,
        tipo_pagamento="PIX",
        cliente="João Silva",
        nota_fiscal="NF-12345"
    )

    template = Template(
        nome="Teste",
        colunas=["Data", "Cliente", "Nota"],
        mapeamento={"Data": "data", "Cliente": "cliente", "Nota": "nota_fiscal"}
    )

    valor_cliente = template.get_valor_mapeado(transaction, "Cliente")
    valor_nota = template.get_valor_mapeado(transaction, "Nota")

    print(f"✅ Valores de extras extraídos:")
    print(f"   Cliente: {valor_cliente}")
    print(f"   Nota: {valor_nota}")

    if valor_cliente == "João Silva" and valor_nota == "NF-12345":
        print("✅ Extras corretos!")
    else:
        print("❌ Extras incorretos!")

except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 10: get_valor_mapeado() com campo inexistente
print("\n=== Teste 10: get_valor_mapeado() - campo inexistente ===")
try:
    transaction = Transaction(
        data="06/10/2025",
        valor=150.50,
        tipo_pagamento="PIX"
    )

    template = Template(
        nome="Teste",
        colunas=["Data", "Cliente"],
        mapeamento={"Data": "data", "Cliente": "cliente"}
    )

    valor_inexistente = template.get_valor_mapeado(transaction, "Cliente")

    if valor_inexistente == "":
        print(f"✅ Campo inexistente retorna vazio: '{valor_inexistente}'")
    else:
        print(f"❌ Deveria retornar vazio, mas retornou: {valor_inexistente}")

except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 11: to_dict()
print("\n=== Teste 11: to_dict() ===")
try:
    template = Template(
        nome="Omie",
        colunas=["Data", "Valor"],
        mapeamento={"Data": "data", "Valor": "valor"},
        formatacao={"cor": "#FF0000"}
    )

    dict_template = template.to_dict()

    print(f"✅ Template convertido para dict:")
    print(f"   {dict_template}")

    if (dict_template["nome"] == "Omie" and
        dict_template["colunas"] == ["Data", "Valor"] and
        dict_template["formatacao"] == {"cor": "#FF0000"}):
        print("✅ Conversão correta!")
    else:
        print("❌ Conversão incorreta!")

except Exception as e:
    print(f"❌ Erro: {e}")

print("\n=== Testes concluídos ===")
