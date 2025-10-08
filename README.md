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
│       │   ├── template_manager.py  # Gerenciamento de templates
│       │   └── output_generator.py  # Geração de planilhas formatadas
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

## 🔄 Status do Projeto

### ✅ Módulos Implementados (MVP)

#### 1. Transaction (models/transaction.py) - ✅ COMPLETO
- Validação de dados obrigatórios (data, tipo_pagamento, valor)
- Suporte a campos extras flexíveis
- Normalização de tipos de pagamento
- Taxa de validação: 100%

#### 2. FileHandler (services/file_handler.py) - ✅ COMPLETO
- Leitura de arquivos .xlsx e .xls
- Suporte para OpenPyXL e xlrd
- Escrita de arquivos Excel
- Validações de caminho e formato

#### 3. SheetProcessor (services/sheet_processor.py) - ✅ COMPLETO
- Identificação automática de cabeçalhos
- Remoção de linhas/colunas vazias
- Desmesclagem de células (ffill)
- Limpeza completa de planilhas

#### 4. DataMapper (services/data_mapper.py) - ✅ COMPLETO
- Identificação inteligente de colunas (keywords)
- Extração de transactions com validação
- Conversão automática de datetime para string
- Taxa de sucesso em testes: 98.9% (94/95 transactions)
- Suporta campos extras dinâmicos

#### 5. TemplateManager (services/template_manager.py) - ✅ COMPLETO
- Salvamento de templates de mapeamento em JSON
- Carregamento de templates salvos
- Listagem de todos os templates disponíveis
- Exclusão de templates
- 8 testes automatizados (100% de aprovação)
- Armazenamento em `data/templates/`

#### 6. Template (models/template.py) - ✅ COMPLETO
- Modelo para definir formatos de saída (Omie, Custom, etc.)
- Validações completas (nome, colunas, mapeamento, formatação)
- Método to_dict() para serialização
- Método get_valor_mapeado() para extração de valores
- 11 testes automatizados (100% de aprovação)
- Suporta campos obrigatórios e extras

#### 7. OutputGenerator (services/output_generator.py) - ✅ COMPLETO
- Função gerar_planilha() para geração de arquivos Excel formatados
- Recebe lista de Transactions + Template e gera planilha no formato desejado
- Validações completas (template, transactions, output_path)
- Suporta campos obrigatórios e extras dinamicamente
- 6 testes automatizados (100% de aprovação)
- Teste end-to-end validando pipeline completo (importar → limpar → extrair → formatar → gerar)

### 🚧 Em Desenvolvimento

#### 8. Interface UI (ui/main_window.py) - ⏳ EM DESENVOLVIMENTO

### 📋 Pendente

#### 9. Banco de Dados (database.py) - ⏳ PLANEJADO
- Layout definido (1366x720)
- Tema dark mode especificado
- Todos os módulos core prontos para integração

- SQLite para histórico de conciliações
- Migração de templates JSON → SQLite (futuro)

---

## 📊 Métricas de Desenvolvimento

- **Linhas de código**: ~900 linhas (sem testes)
- **Testes implementados**: 7 arquivos (test_file_handler, test_sheet_processor, test_data_mapper, test_template_manager, test_template, test_output_generator, test_end_to_end)
- **Total de testes**: 34 testes automatizados
- **Cobertura de testes**: Pipeline completo testado end-to-end (100% dos módulos core)
- **Taxa de sucesso em dados reais**: 98.9%
- **Documentação**: 100% dos módulos implementados documentados

---

## 🔄 Changelog

### v2.0.0 (Em desenvolvimento - 06/10/2025)

#### ✅ Completado
- ✅ Refatoração completa da arquitetura
- ✅ Separação de responsabilidades (Models, Services, UI)
- ✅ Sistema de validação robusto (Transaction)
- ✅ Processamento inteligente de planilhas (SheetProcessor)
- ✅ Mapeamento flexível de dados (DataMapper)
- ✅ **TemplateManager completo** (save, load, list, delete)
- ✅ **Template model completo** (to_dict, get_valor_mapeado)
- ✅ **OutputGenerator completo** (gerar_planilha)
- ✅ Sistema de templates de mapeamento em JSON
- ✅ Sistema de templates de saída (Omie, Custom, etc.)
- ✅ Suporte para múltiplos formatos Excel (.xlsx, .xls)
- ✅ Pipeline completo de testes (7 módulos, 34 testes, incluindo end-to-end)
- ✅ Documentação técnica completa
- ✅ Teste end-to-end validando todo o fluxo

#### ⏳ Próximos Passos
- Interface UI modernizada (ui/main_window.py)
- Integração dos módulos core na UI
- Banco de dados SQLite para histórico (futuro)

### v1.0.0
- Versão inicial
- Processamento básico de planilhas
- Interface gráfica com CustomTkinter
- Banco de dados SQLite para histórico

## 📞 Suporte

Para suporte, abra uma [issue](https://github.com/seu-usuario/conciliador-financeiro/issues) no GitHub.

---

