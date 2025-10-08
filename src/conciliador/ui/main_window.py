import customtkinter as ctk
# Importa a nova classe controller
from .ui_controller import UIController

ctk.set_appearance_mode("system")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Cria uma instância do controller, passando a view (self)
        self.controller = UIController(self)

        # --- Configurações da Janela Principal ---
        self.title("Conciliador")
        self.geometry("1366x768")

        # --- Estrutura da Grelha Principal (Layout) ---
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Construção da Interface ---
        self.criar_header()
        self.criar_area_central()

    # ==================================================================================
    # HEADER
    # ==================================================================================
    def criar_header(self):
        """Cria o container do cabeçalho com o logo e o título da aplicação."""

        # O container do header ocupa a primeira linha (row=0) da grelha principal.
        container_header = ctk.CTkFrame(self, height=100, corner_radius=0, fg_color="transparent")
        container_header.grid(row=0, column=0, sticky="ew")
        container_header.grid_propagate(False)

        # Grelha interna do header para alinhar os elementos.
        # As colunas das pontas (0 e 2) têm o mesmo peso para centralizar o título (coluna 1).
        container_header.grid_rowconfigure(0, weight=1)
        container_header.grid_columnconfigure((0, 2), weight=1)
        container_header.grid_columnconfigure(1, weight=0)

        logo_label = ctk.CTkLabel(container_header, text="DomaGrupo", font=("Sans-serif", 18))
        logo_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")

        title_label = ctk.CTkLabel(container_header, text="Conciliador Financeiro", font=("Sans-serif", 18))
        title_label.grid(row=0, column=1, pady=10, sticky="ew")

    # ==================================================================================
    # ÁREA CENTRAL
    # ==================================================================================
    def criar_area_central(self):
        """Cria a área de trabalho principal que contém os frames esquerdo, direito e central."""
        
        # O frame principal da área de trabalho, ocupa a segunda linha (row=1).
        core_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        core_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Grelha interna para dividir a área de trabalho em 3 colunas proporcionais.
        core_frame.grid_rowconfigure(0, weight=1)
        core_frame.grid_columnconfigure(0, weight=35) # Frame Esquerdo
        core_frame.grid_columnconfigure(1, weight=40) # Centro
        core_frame.grid_columnconfigure(2, weight=25) # Frame Direito

        self.criar_frame_esquerdo(parent=core_frame)
        self.criar_frame_direito(parent=core_frame)
        self.criar_area_importacao(parent=core_frame)

    # ----------------------------------------------------------------------------------
    # Sub-componentes da Área Central
    # ----------------------------------------------------------------------------------
    def criar_frame_esquerdo(self, parent):
        """Cria o painel de configurações à esquerda."""
        left_frame = ctk.CTkFrame(parent, corner_radius=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        # Usaremos .pack() para organizar os widgets verticalmente dentro deste frame.
        # O 'padx' e 'pady' garantem um bom espaçamento.
        
        config_Title = ctk.CTkLabel(left_frame, text="Configurações de Importação", font=("Sans-serif", 14))
        config_Title.pack(pady=10)
        config_title = ctk.CTkLabel(left_frame, text="Configurações de Importação", font=("Sans-serif", 16, "bold"))
        config_title.pack(pady=(15, 20), padx=20)

        # --- Seção de Templates de Mapeamento ---
        # Conforme a documentação, o TemplateManager gerencia templates de mapeamento.
        # Este OptionMenu permitirá ao usuário escolher qual template usar.
        template_label = ctk.CTkLabel(left_frame, text="Template de Mapeamento:", anchor="w")
        template_label.pack(pady=(10, 5), padx=20, fill="x")

        # A view não busca mais os dados, ela apenas é construída.
        # A lógica de carregar os templates será chamada pelo controller.
        templates_disponiveis = ["Automático", "Banco Inter", "Nubank"]

        # A ação do menu é delegada para o controller.
        template_option_menu = ctk.CTkOptionMenu(
            left_frame,
            values=templates_disponiveis,
            command=self.controller.on_template_select
        )
        template_option_menu.pack(pady=(0, 20), padx=20, fill="x")

        # ONDE PROGRAMAR (5): Ler o estado deste checkbox.
        # Após o `DataMapper` retornar a lista de erros, verifique o estado com `log_checkbox.get()`.
        # Se estiver marcado, escreva os erros em um arquivo de log.
        log_checkbox = ctk.CTkCheckBox(left_frame, text="Salvar log de erros")
        log_checkbox.pack(pady=(20, 10), padx=20, fill="x")


    def criar_frame_direito(self, parent):
        """Cria o painel de histórico rolável à direita."""
        right_frame = ctk.CTkScrollableFrame(parent, corner_radius=20)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        
        scroll_Title = ctk.CTkLabel(right_frame, text="Últimas Conciliações:", font=("Sans-serif", 14))
        scroll_Title.pack(pady=10)




    def criar_area_importacao(self, parent):
        """Cria a área central para importação de ficheiros."""
        
        center_frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="transparent")
        center_frame.grid(row=0, column=1, sticky="nsew")

        # Frame decorativo para o botão de importação.
        import_frame = ctk.CTkFrame(center_frame, height=200, width=250, corner_radius=50)
        import_frame.place(relx=0.5, rely=0.5, anchor="center")

        import_label = ctk.CTkLabel(import_frame, text="Importe aqui suas planilhas Excel:", font=("Sans-serif", 14))
        import_label.place(relx=0.5, rely=0.4, anchor="center")

        # A ação do botão é delegada para o controller.
        importButton = ctk.CTkButton(
            import_frame,
            text="Importar",
            corner_radius=40,
            command=self.controller.iniciar_processo_importacao)
        importButton.place(relx=0.5, rely=0.75, anchor="center")

    def run(self):
        self.mainloop() 

if __name__ == "__main__":
    app = MainWindow()
    app.run()
