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

    # Garantir que o diretório de templates existe, se não, criar
    os.makedirs(TEMPLATE_DIR, exist_ok=True)

    # Define a data atual
    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Padroniza o nome do arquivo

    nome = nome.lower().replace(" ", "_")


    json.dump_data = {
        "nome": nome,
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mapping": {
            "data": "data",
            "tipo_pagamento" : "tipo_pagamento",
            "valor" : "valor",
        }
    }


def load_template(nome):
    '''
    Carrega um template de mapeamento de um arquivo JSON.
    '''

def list_templates():
    '''
    Lista todos os templates de mapeamento disponíveis.
    '''

def delete_template(nome):
    '''
    Deleta um template de mapeamento.
    '''

