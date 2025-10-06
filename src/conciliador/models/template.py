
# Definição da classe Template

class Template:
    '''
    Classe que representa um template de saída para exportação de dados.
    '''

    def __init__(self, nome, colunas, mapeamento, formatacao = None):
        '''
        Inicializa um objeto Template.

        Parâmetros:
        nome (str): Nome do template.
        colunas (list): Lista de colunas do template.
        mapeamento (dict): Dicionário que mapeia os campos de entrada para as colunas do template.
        formatacao (dict, opcional): Dicionário que define a formatação das colunas. Padrão é None.
        '''
        # Validação dos parâmetros

        # Validação do nome
        if not isinstance(nome, str):
            raise TypeError("O nome do template deve ser uma string.")
        if nome == "":
            raise ValueError("O nome do template não pode ser vazio.")
        
        # Validação das colunas
        if not isinstance(colunas, list) or not all(isinstance(coluna, str) for coluna in colunas):
            raise TypeError("As colunas devem ser uma lista de strings.")
        if colunas == []:
            raise ValueError("A lista de colunas não pode ser vazia.")
        
        # Validação do mapeamento
        if not isinstance(mapeamento, dict) or not all(isinstance(chave, str) and isinstance(valor, str) for chave, valor in mapeamento.items()):
            raise TypeError("O mapeamento deve ser um dicionário com chaves e valores do tipo string.")
        if mapeamento == {}:
            raise ValueError("O dicionário de mapeamento não pode ser vazio.")
        
        # Validação da formatação
        if formatacao is not None and (not isinstance(formatacao, dict) or not all(isinstance(chave, str) and isinstance(valor, str) for chave, valor in formatacao.items())):
            raise TypeError("A formatação deve ser um dicionário com chaves e valores do tipo string ou None.")
        
        # Verificação de equivalência entre colunas e valores do mapeamento
        chaves_colunas = set(colunas)
        chaves_mapeamento = set(mapeamento.keys())
        if chaves_mapeamento != chaves_colunas:
            raise ValueError("As colunas e os valores do mapeamento devem ser equivalentes.")
        
        # Atribuição dos atributos
    
        self.nome = nome
        self.colunas = colunas
        self.mapeamento = mapeamento
        self.formatacao = formatacao if formatacao is not None else {}

    def to_dict(self):
        '''
        Converte o objeto Template em um dicionário.

        Retorna:
        dict: Dicionário representando o objeto Template.
        '''
        return {
            "nome": self.nome,
            "colunas": self.colunas,
            "mapeamento": self.mapeamento,
            "formatacao": self.formatacao
        }
    def get_valor_mapeado(self, transaction, coluna):
        '''
        Retorna o valor mapeado para uma chave específica.

        Parâmetros:
        chave (str): Chave para a qual se deseja obter o valor mapeado.

        Retorna:
        str: Valor mapeado correspondente à chave.
        '''
        # Pega o nome do campo mapeado
        campo = self.mapeamento[coluna]

        if hasattr(transaction, campo):
            return getattr(transaction, campo)
        if campo in transaction.extras:
            return transaction.extras[campo]
        
        return ""
    

        