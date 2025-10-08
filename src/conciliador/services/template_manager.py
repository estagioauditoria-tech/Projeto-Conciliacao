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
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do template não pode ser vazio.")
    if not isinstance(mapping, dict) or not mapping:
        raise ValueError("O mapeamento não pode ser um dicionário vazio.")

    # Garantir que o diretório de templates existe, se não, criar
    os.makedirs(TEMPLATE_DIR, exist_ok=True)

    # Padroniza o nome do arquivo para ser usado como nome de arquivo
    file_name = nome.strip().lower().replace(" ", "_")
    file_path = os.path.join(TEMPLATE_DIR, f"{file_name}.json")

    # Estrutura de dados a ser salva, conforme a documentação
    template_data = {
        "nome": nome,
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mapping": mapping
    }

    # Salva o arquivo JSON
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(template_data, file, indent=4, ensure_ascii=False)

    return file_path

def load_template(nome):
    '''
    Carrega um template de mapeamento de um arquivo JSON.
    Retorna o dicionário do template ou None se não encontrado.
    '''
    # Padroniza o nome do arquivo e carrega ele
    file_name = nome.strip().lower().replace(" ", "_")
    file_path = os.path.join(TEMPLATE_DIR, f"{file_name}.json")

    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return None # Retorna None se o arquivo estiver corrompido ou ilegível
    else:
        return None

def list_templates():
    '''
    Lista todos os templates de mapeamento disponíveis.
    Retorna uma lista com os nomes dos templates.
    '''
    # Verifica se o arquivo existe
    if not os.path.exists(TEMPLATE_DIR):
        return []
    
    # Cria uma lista vazia para salvar a lista de templates
    templates = []

    # Itera sobre os arquivos no diretório
    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith(".json"):
            # Remove a extensão .json para obter o nome do template
            template_name = filename[:-5].replace("_", " ").title()
            templates.append(template_name)
    
    return sorted(templates)

def delete_template(nome):
    '''
    Deleta um template de mapeamento.
    Retorna True se o arquivo foi deletado, False caso contrário.
    '''
    # Padroniza o nome dos arquivos e carrega eles
    file_name = nome.strip().lower().replace(" ", "_")
    file_path = os.path.join(TEMPLATE_DIR, f"{file_name}.json")

    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        try:
            os.remove(file_path) # Deleta o arquivo
            return True
        except OSError:
            return False
    return False
