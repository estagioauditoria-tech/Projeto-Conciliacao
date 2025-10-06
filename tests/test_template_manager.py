# test_template_manager.py
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from conciliador.services.template_manager import save_template, load_template, list_templates, delete_template

# Teste 1: Salvar template válido
print("=== Teste 1: Salvar template válido ===")
mapping = {
    "data": "Data Lançamento",
    "tipo": "Forma Pagamento",
    "valor": "Valor Total"
}

try:
    resultado = save_template("Banco Inter", mapping)
    print(f"✅ Template salvo em: {resultado}")
except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 2: Carregar template
print("\n=== Teste 2: Carregar template ===")
try:
    mapping_carregado = load_template("Banco Inter")
    print(f"✅ Template carregado: {mapping_carregado}")

    # Verifica se o mapping está correto
    if mapping_carregado == mapping:
        print("✅ Mapping carregado é idêntico ao original!")
    else:
        print("❌ Mapping diferente do original!")
except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 3: Carregar template inexistente (deve dar erro)
print("\n=== Teste 3: Template inexistente (deve dar erro) ===")
try:
    resultado = load_template("Template Que Nao Existe")
    print(f"❌ Não deveria ter funcionado!")
except FileNotFoundError as e:
    print(f"✅ Erro capturado corretamente: {e}")

# Teste 4: Validação - nome vazio
print("\n=== Teste 4: Nome vazio (deve dar erro) ===")
try:
    resultado = save_template("", mapping)
    print(f"❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado corretamente: {e}")

# Teste 5: Validação - mapping sem campo obrigatório
print("\n=== Teste 5: Mapping incompleto (deve dar erro) ===")
mapping_incompleto = {"data": "Data"}
try:
    resultado = save_template("Teste", mapping_incompleto)
    print(f"❌ Não deveria ter funcionado!")
except ValueError as e:
    print(f"✅ Erro capturado corretamente: {e}")

# Teste 6: Listar templates
print("\n=== Teste 6: Listar templates ===")
try:
    templates = list_templates()
    print(f"✅ Templates encontrados ({len(templates)}): {templates}")

    if "banco_inter" in templates:
        print("✅ Template 'banco_inter' está na lista!")
    else:
        print("❌ Template 'banco_inter' não encontrado na lista!")
except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 7: Deletar template
print("\n=== Teste 7: Deletar template ===")
try:
    # Primeiro salva um template de teste
    save_template("Template Para Deletar", mapping)
    print("✅ Template de teste criado")

    # Verifica que existe
    templates_antes = list_templates()
    if "template_para_deletar" in templates_antes:
        print("✅ Template existe antes de deletar")

    # Deleta o template
    resultado = delete_template("Template Para Deletar")
    print(f"✅ Template deletado: {resultado}")

    # Verifica que foi deletado
    templates_depois = list_templates()
    if "template_para_deletar" not in templates_depois:
        print("✅ Template foi removido da lista!")
    else:
        print("❌ Template ainda está na lista!")

except Exception as e:
    print(f"❌ Erro: {e}")

# Teste 8: Deletar template inexistente (deve dar erro)
print("\n=== Teste 8: Deletar template inexistente (deve dar erro) ===")
try:
    delete_template("Template Inexistente")
    print(f"❌ Não deveria ter funcionado!")
except FileNotFoundError as e:
    print(f"✅ Erro capturado corretamente: {e}")

print("\n=== Testes concluídos ===")
