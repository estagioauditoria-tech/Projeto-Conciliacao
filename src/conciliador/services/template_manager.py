# Importações
import os
import json
from datetime import datetime

TEMPLATE_DIR = os.path.join("data", "templates")

 # Funções:
  # - salvar_template(nome, mapping) ->save_template
  # - carregar_template(nome) ->load_template
  # - listar_templates() ->list_templates
  # - deletar_template(nome) ->delete_template



def save_template(nome, mapping):
    '''
    Salva um template de mapeamento em um arquivo JSON.
    '''
    # Validações 

    # Validação 1 - nome
    if not isinstance(nome, str):
        raise TypeError("O nome do template deve ser uma string.")
    if not nome.strip():
        raise ValueError("O nome do template não pode ser vazio.")
    # Validação 2 - mapping
    if not isinstance(mapping, dict):
        raise TypeError("O mapeamento deve ser um dicionário.")
    # Validação 3 - chaves do mapping
    validate_keys = {"data", "tipo", "valor"}
    for key in validate_keys:
        if key not in mapping:
            raise ValueError (f"A chave '{key}' é obrigatória no mapeamento.")
            
        # Cria o diretório se não existir
    if not os.path.exists(TEMPLATE_DIR):
        os.makedirs(TEMPLATE_DIR)
    
    # Salva o template
    arquive_name = nome.replace(" ", "_").lower().strip()
    template_path = os.path.join(TEMPLATE_DIR, f"{arquive_name}.json")

    # Cria dicionário do template
    template_data = {
        "nome": nome,
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "mapping": mapping
    }
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(template_data, f, ensure_ascii=False, indent=4)
    
    return template_path

def load_template(nome):
    '''
    Carrega um template de mapeamento de um arquivo JSON.
    '''
    # Validações
    if not isinstance(nome, str):
        raise TypeError("O nome do template deve ser uma string.")
    if not nome.strip():
        raise ValueError("O nome do template não pode ser vazio.")
     
    # Padroniza
    arquive_name = nome.replace(" ", "_").lower().strip()
    template_path = os.path.join(TEMPLATE_DIR, f"{arquive_name}.json")

    # Verifica se o arquivo existe
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"O template '{nome}' não foi encontrado.")
    
    # Carrega o template
    with open(template_path, "r", encoding="utf-8") as f:
        template_data = json.load(f)
    
    return template_data["mapping"]


def list_templates():
    '''
    Lista todos os templates de mapeamento disponíveis.
    '''
    # Verifica se o diretório existe
    if not os.path.exists(TEMPLATE_DIR):
        return []
    # Lista os arquivos JSON no diretório
    archives = os.listdir(TEMPLATE_DIR)
    templates = []

    for archive in archives:
        if archive.endswith(".json"):
            nome = archive.replace(".json", "")
            templates.append(nome)

    return templates



def delete_template(nome):
    '''
    Deleta um template de mapeamento.
    '''

    # Validações
    if not isinstance(nome, str):
        raise TypeError("O nome do template deve ser uma string.")
    if not nome.strip():
        raise ValueError("O nome do template não pode ser vazio.")
    
    # Padroniza
    arquive_name = nome.replace(" ", "_").lower().strip()
    template_path = os.path.join(TEMPLATE_DIR, f"{arquive_name}.json")

    # Verifica se o arquivo existe
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"O template '{nome}' não foi encontrado.")
    
    # Deleta o arquivo
    os.remove(template_path)
    
    return True

