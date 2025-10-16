import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para que os módulos possam ser encontrados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conciliador.ui.main_window import MainWindow

# Inicia a Aplicação

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
    