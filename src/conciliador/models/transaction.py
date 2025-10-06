# Importações
import tkinter as tk


TIPOS_DE_TRANSACAO = [
    # Crédito
    ("crédito", "CRÉDITO"),
    ("credito", "CRÉDITO"),
    ("CRÉDITO", "CRÉDITO"),
    ("CREDITO", "CRÉDITO"),
    # Débito
    ("débito", "DÉBITO"),
    ("debito", "DÉBITO"),
    ("DÉBITO", "DÉBITO"),
    ("DEBITO", "DÉBITO"),
    # Conveniado
    ("conveniado", "CONVENIADO"),
    ("convenio", "CONVENIADO"),
    ("CONVENIADO", "CONVENIADO"),
    ("CONVENIO", "CONVENIADO"),
    # Pix
    ("pix", "PIX"),
    ("PIX", "PIX"),
    # Dinheiro
    ("dinheiro", "DINHEIRO"),
    ("cash", "DINHEIRO"),
    ("DINHEIRO", "DINHEIRO"),
    ("CASH", "DINHEIRO"),
]

# Classe Transaction
class Transaction:
    '''
    Classe que representa uma transação financeira.
    '''

    def __init__(self, data, tipo_pagamento , valor, **extras):
        '''
        Construtor da classe Transaction.
        '''

        # Chama função de validação
        self._validate(data, tipo_pagamento , valor)

        # Atributos
        self.data = data # Tipo: str
        self.tipo_pagamento = tipo_pagamento # Tipo: str
        self.valor = valor # Tipo: float
        self.extras = extras # Tipo: dict

        pass

    def _validate(self, data, tipo_pagamento , valor):
        '''
        Função que valida os atributos da classe Transaction.
        '''

        # Validação da data
        if not isinstance(data, str):
            raise TypeError("A data deve ser uma string no formato 'DD/MM/AAAA'.")
        if len(data) != 10 or data[2] != '/' or data[5] != '/':
            raise ValueError("A data deve estar no formato 'DD/MM/AAAA'.")
        dia, mes, ano = data.split('/')
        if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
            raise ValueError("A data deve conter apenas números e barras no formato 'DD/MM/AAAA'.")
        
        # Validação do tipo de pagamento
        if not isinstance(tipo_pagamento, str):
            raise TypeError("O tipo de pagamento deve ser uma string.")
        tipo_pagamento = tipo_pagamento.strip().lower()
        tipos_validos = [tipo[0] for tipo in TIPOS_DE_TRANSACAO]
        if tipo_pagamento not in tipos_validos:
            raise ValueError(f"O tipo de pagamento '{tipo_pagamento}' é inválido. Tipos válidos: {', '.join(tipos_validos)}.")
        
        # Normaliza o tipo de pagamento
        for tipo in TIPOS_DE_TRANSACAO:
            if tipo_pagamento == tipo[0]:
                tipo_pagamento = tipo[1]
                break
        
        # Validação do valor
        if not isinstance(valor, (int, float)):
            raise TypeError("O valor deve ser um número (int ou float).")
        if valor < 0:
            raise ValueError("O valor não pode ser negativo.")
        if isinstance(valor, int):
            valor = float(valor)
        if round(valor, 2) != valor:
            raise ValueError("O valor deve ter no máximo duas casas decimais.")
        pass
        return True
        
def campo_extra(**kwargs):
    '''
    Função que adiciona os campos extras do usuário
    no dicionário de transações.
    '''

    extras = {}
    for key, value in kwargs.items():
        if isinstance(value, (str, int, float)):
            extras[key] = value
        else:
            raise TypeError("Os campos extras devem ser do tipo str, int ou float.")
    return extras

def to_dict(Transaction):
    '''
    Função que converte um objeto Transaction em um dicionário.
    '''

    # Dicionário
    transaction_dict = {
        "data": Transaction.data,
        "tipo": Transaction.tipo,
        "valor": Transaction.valor,
    }

    # Adiciona os campos extras
    transaction_dict.update(Transaction.extras)

    return transaction_dict
