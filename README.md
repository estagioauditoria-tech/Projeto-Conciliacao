# Conciliador Financeiro v2

> Sistema automatizado de conciliação financeira com processamento inteligente de planilhas e geração de relatórios padronizados.

## 📋 Visão Geral

O Conciliador Financeiro é uma aplicação desktop desenvolvida em Python que automatiza o processo de conciliação de transações financeiras. O sistema processa planilhas de diferentes fontes, normaliza os dados e gera relatórios no formato desejado (Omie, customizado, etc.), reduzindo drasticamente o tempo de processamento manual.

**Principais Benefícios:**
- ⏱️ Redução de tempo: de 3 horas para poucos minutos
- 🎯 Precisão: eliminação de erros manuais
- 🔄 Flexibilidade: suporta múltiplos formatos de entrada e saída
- 🎨 Interface moderna: design responsivo e intuitivo

## ✨ Funcionalidades

- **Importação Inteligente**: Suporte para múltiplos formatos (XLSX, XLS, CSV)
- **Processamento Automatizado**: Limpeza e normalização de dados
- **Classificação de Transações**: Identificação automática de tipos de pagamento (PIX, Cartão, Dinheiro, etc.)
- **Templates Customizáveis**: Geração de relatórios em formatos personalizados
- **Histórico Completo**: Registro de todas as operações realizadas
- **Validação de Dados**: Verificação automática de inconsistências

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas com separação clara de responsabilidades:

```
src/conciliador/
├── models/              # Modelos de dados (Transaction, Template)
├── services/            # Lógica de negócio (processamento, mapeamento)
├── ui/                  # Interface gráfica (CustomTkinter)
└── utils/               # Utilitários e validadores
```

### Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **Pandas**: Manipulação e análise de dados
- **OpenPyXL**: Processamento de arquivos Excel
- **CustomTkinter**: Interface gráfica moderna
- **SQLite**: Banco de dados local para histórico

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/conciliador-financeiro.git
cd conciliador-financeiro
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Uso

### Executar a Aplicação

```bash
python -m src.conciliador.ui.main_window
```

### Fluxo Básico de Uso

1. **Importar Planilha**: Clique em "Importar" e selecione o arquivo
2. **Processamento Automático**: O sistema normaliza e valida os dados
3. **Geração de Relatório**: Planilha formatada é gerada automaticamente
4. **Visualizar Histórico**: Acesse o painel lateral para ver operações anteriores

## 📂 Estrutura do Projeto

```
conciliador-financeiro/
├── src/
│   └── conciliador/
│       ├── models/              # Definições de dados
│       │   ├── transaction.py   # Modelo de transação
│       │   └── template.py      # Modelo de template
│       ├── services/            # Lógica de negócio
│       │   ├── file_handler.py      # Importação/exportação
│       │   ├── sheet_processor.py   # Processamento de planilhas
│       │   ├── data_mapper.py       # Mapeamento de dados
│       │   └── template_manager.py  # Gerenciamento de templates
│       ├── ui/                  # Interface gráfica
│       │   ├── main_window.py   # Janela principal
│       │   └── styles.py        # Estilos e temas
│       └── utils/               # Utilitários
│           └── validators.py    # Validações
├── docs/                    # Documentação detalhada
├── data/                    # Templates e arquivos de configuração
├── tests/                   # Testes automatizados
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src
```

## 📚 Documentação

Documentação completa disponível em [`docs/documentacao.md`](docs/documentacao.md)

### Tópicos da Documentação

- Arquitetura detalhada do sistema
- Guia de desenvolvimento
- API de referência
- Exemplos de uso avançado
- Troubleshooting

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Padrão de Commits

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `refactor:` Refatoração de código
- `test:` Adição de testes
- `chore:` Manutenção

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Paulo Ygor** - Estagiário | Grupo Doma - Desenvolvimento e arquitetura

## 🔄 Changelog

### v2.0.0 (Em desenvolvimento)
- Refatoração completa da arquitetura
- Separação de responsabilidades (Models, Services, UI)
- Suporte para múltiplos templates
- Sistema de validação robusto
- Interface modernizada

### v1.0.0
- Versão inicial
- Processamento básico de planilhas
- Interface gráfica com CustomTkinter
- Banco de dados SQLite para histórico

## 📞 Suporte

Para suporte, abra uma [issue](https://github.com/seu-usuario/conciliador-financeiro/issues) no GitHub.

---

