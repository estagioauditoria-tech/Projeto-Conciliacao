# Importações 
from ..models.transaction import Transaction

# Lista de Sinônimos
data_keywords = ["data", "dt", "date", "data da transação", "data lançamento", "data_movimento", "data_transacao"]
tipo_keywords = [
    "tipo", "tipo de transação", "transação", "transacao", "natureza", "categoria", 
    "descrição", "descricao", "forma de pagamento", "meio de pagamento", "método de pagamento", 
    "metodo de pagamento", "pagamento", "transferência", "transferencia"
]
valor_keywords = ["valor", "valor da transação", "valor_transacao", "quantia", "montante", "total", "amount"]


#----------Módulo para mapear dados do DataFrame para objetos Transaction-------------#

    ###Função de identificação de colunas

def column_identifier(df):
    '''
    Identifica as colunas necessárias no DataFrame e retorna um dicionário com os nomes das colunas.
    As colunas obrigatórias são extraídas do modelo Transaction.
    (Data, Tipo, Valor)
    '''
    mapping = {
        "data": None,
        "tipo": None,
        "valor": None
    }

    # Mapeia as colunas obrigatórias
    try:

        for coluna in df.columns:
            coluna_lower = coluna.strip().lower()   # Normaliza o nome da coluna para comparação

        # Verifica se a coluna corresponde a algum dos sinônimos
            if any(keyword in coluna_lower for keyword in data_keywords):
                mapping["data"] = coluna
            elif any(keyword in coluna_lower for keyword in tipo_keywords):
                mapping["tipo"] = coluna
            elif any(keyword in coluna_lower for keyword in valor_keywords):
                mapping["valor"] = coluna
              
        # Verifica se todas as colunas obrigatórias foram encontradas
        
        if mapping["data"] is None:
            raise ValueError("Coluna de data não encontrada.")
        if mapping["tipo"] is None:
            raise ValueError("Coluna de tipo de pagamento não encontrada.")
        if mapping["valor"] is None:
            raise ValueError("Coluna de valor não encontrada.")
                
        return mapping
        
    except Exception as e:
        raise ValueError(f"Erro ao identificar colunas: {e}")

    ###Função de extração de transações

def extract_transactions(df):
    """
Converte DataFrame em lista de Transactions.
Retorna (lista_sucessos, lista_erros).
    """
    mapping = column_identifier(df)
    success_list = []
    error_list = []

        # Itera pelas linhas do DataFrame e cria objetos Transaction
    for index, row in df.iterrows():
        try: 
            # Extrai os valores das colunas obrigatórias
            data = row[mapping["data"]]     
            if hasattr(data, 'strftime'):  # Se é datetime
                data = data.strftime('%d/%m/%Y')
            elif not isinstance(data, str):  # Se não é string nem datetime
                data = str(data)
            
            tipo = row[mapping["tipo"]]
            valor = row[mapping["valor"]]

            # Extrai os valores das colunas extras
            extras = {}
            for col in df.columns:
                if col not in mapping.values():
                    extras[col] = row[col]

            # Cria o objeto Transaction
            transaction = Transaction(data=data, tipo_pagamento=tipo, valor=valor, **extras)
            success_list.append(transaction)

        except Exception as e:
            error_list.append((f"Linha {index}: {e}"))

    return success_list, error_list
