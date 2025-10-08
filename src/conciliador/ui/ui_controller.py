# Importações do sistema e de bibliotecas
from tkinter import filedialog
import os
from datetime import datetime
import pandas as pd

# Importações dos módulos do projeto (camada de serviços)
# Usando caminhos relativos a partir da estrutura do projeto
from ..services import file_handler
from ..services import sheet_processor
from ..services import data_mapper
from ..services import template_manager
from ..services import output_generator

# Importações dos modelos de dados
from ..models.transaction import Transaction
from ..models.template import Template

# Importação da View para type hinting
# Usamos 'if TYPE_CHECKING' para evitar importação circular em tempo de execução
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .main_window import MainWindow


class UIController:
    def __init__(self, view: "MainWindow"):
        """
        Inicializa o Controller.

        Args: 
            view: A instância da MainWindow (a View) que este controller gerencia.
        """
        self.view = view
        self.template_selecionado = "Automático" # Valor padrão

    def iniciar_processo_importacao(self):
        """
        Orquestra todo o fluxo de importação e processamento de uma planilha.
        Este método é o "maestro" chamado pelo botão 'Importar'.
        """
        try:
            print("Iniciando processo de importação...")
            # 1. Abrir diálogo de arquivo para pegar o caminho
            caminho = filedialog.askopenfilename(
                title="Selecione a planilha",
                filetypes=[("Planilhas Excel", "*.xlsx *.xls"), ("Todos os arquivos", "*.*")]
            )

            if not caminho: # Verifica se o usuário cancelou a seleção
                print("Nenhum arquivo selecionado. Processo cancelado.")
                # Aqui você poderia atualizar a UI para mostrar uma mensagem ao usuário
                return

            print(f"Caminho selecionado: {caminho}")

            # 2. Chamar file_handler
            df = file_handler.read_file(caminho)
            print(f"Arquivo lido com sucesso! Dimensões: {df.shape}")

            # 3. Chamar sheet_processor
            df_limpo = sheet_processor.clean_sheet(df)
            print("Planilha limpa com sucesso!")

            # 4. Chamar data_mapper
            transactions, erros = data_mapper.extract_transactions(df_limpo)
            print(f"Transações extraídas: {len(transactions)} sucesso, {len(erros)} erros.")

            # 5. Preparar um objeto Template para a geração de saída
            #    - se o usuário escolher um template salvo, carregamos ele via template_manager
            #    - caso contrário usamos um template "Automático" padrão
            try:
                if self.template_selecionado != "Automático":
                    loaded = template_manager.load_template(self.template_selecionado)
                    if loaded is None:
                        raise ValueError(f"Template '{self.template_selecionado}' não encontrado.")
                    mapping = loaded.get("mapping", {})
                    # As colunas do template são as chaves do mapping salvo
                    colunas = list(mapping.keys())
                    template = Template(loaded.get("nome", self.template_selecionado), colunas, mapping, loaded.get("formatacao"))
                else:
                    # Template automático: mapeia colunas padrão para atributos do Transaction
                    default_mapping = {"Data": "data", "Tipo": "tipo_pagamento", "Valor": "valor"}
                    template = Template("Automático", list(default_mapping.keys()), default_mapping)
            except Exception as e:
                # Propaga como erro mais descritivo para a camada superior/log
                raise RuntimeError(f"Erro ao preparar o template de saída: {e}")

            # Define pasta de saída padrão dentro do projeto
            output_dir = os.path.join("data", "saved_files")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"conciliacao_{timestamp}.xlsx"
            caminho_saida = os.path.join(output_dir, output_filename)

            caminho_saida = output_generator.gerar_planilha(transactions, template, caminho_saida)
            print(f"Planilha gerada em: {caminho_saida}")

            # 6. Atualizar a view com o resultado
            print("Processo finalizado com sucesso!")
            # self.view.mostrar_sucesso(len(transactions), len(erros))

            # >>> PONTO DE EXTENSÃO: Se quiser mostrar a planilha gerada diretamente
            # no frame scroll da direita, aqui é o lugar ideal para:
            # 1) ler o arquivo gerado (pandas.read_excel(caminho_saida))
            # 2) chamar uma função da View/Controller que renderiza o DataFrame no
            #    frame de scroll direito (ver `database.py` para instruções)
            
            # Lê o arquivo de saída recém-criado para exibi-lo na UI
            if os.path.exists(caminho_saida):
                df_saida = pd.read_excel(caminho_saida, index_col=0) # index_col=0 para não ler o índice salvo pelo pandas
                self.view.renderizar_planilha_no_frame(df_saida)
        except Exception as e:
            print(f"ERRO no processo de importação: {e}")
            # self.view.mostrar_erro(str(e))

    def on_template_select(self, escolha: str):
        """
        Callback para quando um template de mapeamento é selecionado no OptionMenu.
        """
        self.template_selecionado = escolha
        print(f"Template de mapeamento alterado para: {self.template_selecionado}")

        # Instruções (comentário didático) para implementar o comportamento de
        # "abrir a planilha ao selecionar" (o que você pediu):
        # 1) Quando o usuário seleciona um template, você pode carregar um
        #    arquivo previamente gerado ou aplicar o template a um DataFrame
        #    de exemplo para exibir como a saída ficaria.
        # 2) Se a intenção é que a seleção abra uma planilha existente, implemente:
        #    - procurar por arquivos recentes gerados com esse template (por exemplo,
        #      armazenados em data/saved_files e com metadados que contenham o nome do template)
        #    - se encontrar, chamar pandas.read_excel(caminho) e em seguida
        #      uma função de renderização para o frame direito (ver `database.py`)
        # 3) Se preferir, ao selecionar o template você pode automaticamente
        #    aplicar o template a um DataFrame carregado (por exemplo, a última
        #    importação) e exibir o resultado imediatamente no frame direito.
        #
        # Pseudocódigo didático:
        # def on_template_select(self, escolha):
        #     caminho = buscar_arquivo_por_template(escolha)
        #     if caminho:
        #         df = pd.read_excel(caminho)
        #         self.view.renderizar_planilha_no_frame(df)
        #     else:
        #         # opcional: aplicar template a um DataFrame em memória
        #         df_preview = aplicar_template_preview(self.ultima_df, escolha)
        #         self.view.renderizar_planilha_no_frame(df_preview)

        # >>> PONTO DE EXTENSÃO: Leitura de uma planilha base (Omie)
        # Se você deseja ler uma planilha base (por exemplo, o modelo Omie) e
        # inserir os dados processados no pipeline nela, siga estas orientações:
        # 1) Crie uma função (na camada de serviços) que abra a planilha base e
        #    retorne seu DataFrame e um 'mapa de colunas' (coluna do Omie -> índice/posição).
        # 2) Permita que o usuário mapeie manualmente quais campos do pipeline
        #    correspondem às colunas do Omie (isso pode ser um diálogo simples
        #    ou uma configuração salva em template).
        # 3) A função que escreve na planilha base deve:
        #    - receber um DataFrame com os dados do pipeline
        #    - gerar um DataFrame resultante cujas colunas sigam a ordem/nome do Omie
        #    - escrever os valores nas linhas apropriadas (p. ex. append ou substituir)
        # 4) Após escrever, salve a planilha base em `data/saved_files` com um sufixo
        #    para indicar que foi populada (ex: omie_preenchida_YYYYMMDD.xlsx) e
        #    renderize-a no frame direito para visualização.

        # Se quiser, posso transformar essas instruções em código (diálogo para
        # mapear campos, função de leitura da planilha Omie e rotina de escrita).