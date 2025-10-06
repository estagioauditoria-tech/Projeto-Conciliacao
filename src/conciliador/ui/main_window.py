import customtkinter as ctk
import styles as st

ctk.set_appearance_mode("dark")
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Conciliador")
        self.geometry("1366x768")

        # Criação dos frames principais
        self.criar_header()
        self.criar_central()
        self.criar_sidebar()


        # Criação dos componentes da interface
    def criar_header(self):
        container_header = ctk.CTkFrame(self, height=50, corner_radius=0)

        title_label = ctk.CTkLabel(container_header, **st.header_style)
        
        title_label.pack(pady=10)

    def criar_central(self):

    def criar_sidebar(self):

    def run(self):
        self.mainloop()