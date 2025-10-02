# 📚 Documentação Técnica - Conciliador Financeiro v2

> Documentação completa do sistema de conciliação financeira automatizada

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Modelos de Dados](#modelos-de-dados)
4. [Camada de Serviços](#camada-de-serviços)
5. [Interface do Usuário](#interface-do-usuário)
6. [Fluxo de Dados](#fluxo-de-dados)
7. [Guia de Desenvolvimento](#guia-de-desenvolvimento)
8. [API de Referência](#api-de-referência)
9. [Exemplos de Uso](#exemplos-de-uso)
10. [Troubleshooting](#troubleshooting)

---

## Visão Geral

### Objetivo do Projeto

O Conciliador Financeiro v2 é um sistema desktop desenvolvido em Python para automatizar o processo de conciliação de transações financeiras. O sistema processa planilhas Excel de múltiplas fontes, normaliza os dados e gera relatórios padronizados.

### Problema Resolvido

Empresas que lidam com múltiplas formas de pagamento (PIX, Cartão, Dinheiro, etc.) precisam consolidar dados de diferentes sistemas em formatos específicos (ex: Omie ERP). Este processo manual pode levar horas e está sujeito a erros humanos.

### Solução Proposta

Sistema automatizado que:
- Importa planilhas de diferentes fontes
- Normaliza e valida dados automaticamente
- Classifica transações por tipo de pagamento
- Gera relatórios no formato desejado
- Mantém histórico de operações

### Benefícios Quantificáveis

- **Redução de tempo**: De 3 horas para ~5 minutos
- **Precisão**: Eliminação de erros de digitação/cópia
- **Escalabilidade**: Processa múltiplos arquivos simultaneamente
- **Rastreabilidade**: Histórico completo de operações

---

## Arquitetura do Sistema

### Princípios de Design

O sistema segue os princípios **SOLID** com ênfase em:

1. **Single Responsibility Principle (SRP)**: Cada classe/módulo tem uma única responsabilidade
2. **Dependency Inversion**: Módulos de alto nível não dependem de implementações específicas
3. **Separation of Concerns**: Frontend, Backend e Dados completamente separados

### Arquitetura em Camadas

```
┌─────────────────────────────────────────────────┐
│          CAMADA DE APRESENTAÇÃO (UI)           │
│  - Interface gráfica (CustomTkinter)           │
│  - Interação com usuário                        │
│  - Feedback visual                              │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│         CAMADA DE SERVIÇOS (Business Logic)    │
│  - Processamento de dados                       │
│  - Regras de negócio                            │
│  - Transformações e validações                  │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│           CAMADA DE MODELOS (Data)             │
│  - Definição de estruturas de dados            │
│  - Validações básicas                           │
│  - Serialização                                 │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│          CAMADA DE PERSISTÊNCIA                │
│  - Banco de dados SQLite                        │
│  - Histórico de operações                       │
└─────────────────────────────────────────────────┘
```

### Estrutura de Diretórios

```
src/conciliador/
│
├── models/                      # CAMADA DE DADOS
│   ├── __init__.py
│   ├── transaction.py           # Modelo de transação financeira
│   └── template.py              # Modelo de template de saída
│
├── services/                    # CAMADA DE NEGÓCIO
│   ├── __init__.py
│   ├── file_handler.py          # Gerencia importação/exportação
│   ├── sheet_processor.py       # Processa e limpa planilhas
│   ├── data_mapper.py           # Mapeia dados para Transaction
│   └── template_manager.py      # Gerencia templates de saída
│
├── ui/                          # CAMADA DE APRESENTAÇÃO
│   ├── __init__.py
│   ├── main_window.py           # Janela principal da aplicação
│   └── styles.py                # Estilos e temas visuais
│
├── utils/                       # UTILITÁRIOS
│   ├── __init__.py
│   └── validators.py            # Funções de validação
│
└── database.py                  # CAMADA DE PERSISTÊNCIA
```

---

## Modelos de Dados

### Transaction (models/transaction.py)

**Responsabilidade**: Representar uma única transação financeira

**Estrutura**:

```python
Transaction:
    - data: datetime | str          # Data da transação
    - valor: float                  # Valor monetário
    - tipo_pagamento: str           # PIX, Cartão, Dinheiro, etc.
    - extras: dict                  # Campos adicionais variáveis
```

**Núcleo Rígido (Obrigatório)**:
- `data`: Data/hora da transação
- `valor`: Valor em decimal (sempre positivo)
- `tipo_pagamento`: Método de pagamento utilizado

**Campos Flexíveis (Opcionais)**:
- `extras`: Dicionário com campos específicos de cada fonte de dados
  - Exemplos: `cliente`, `nota_fiscal`, `placa_veiculo`, `cnpj`, etc.

**Validações**:
- Valor deve ser > 0
- Tipo de pagamento deve estar em lista pré-definida
- Data não pode ser vazia

**Métodos**:
- `to_dict()`: Serializa para dicionário
- `_validar()`: Valida dados internos (privado)

### Template (models/template.py)

**Responsabilidade**: Definir estrutura de templates de saída

**Estrutura**:

```python
Template:
    - nome: str                     # Nome do template (ex: "Omie", "Custom")
    - colunas: list[str]            # Lista de colunas esperadas
    - mapeamento: dict              # Mapeamento de campos Transaction → Template
    - formatacao: dict              # Regras de formatação
```

**Atributos**:
- `nome`: Identificador único do template
- `colunas`: Lista ordenada de colunas da planilha final
- `mapeamento`: Como campos de Transaction viram colunas do template
- `formatacao`: Regras de estilo (cores, larguras, etc.)

**Exemplo de Mapeamento**:
```python
{
    "Data": "data",                    # Coluna "Data" vem de transaction.data
    "Valor": "valor",
    "Forma de Pagamento": "tipo_pagamento"
}
```

---

## Camada de Serviços

### FileHandler (services/file_handler.py)

**Responsabilidade**: Gerenciar importação e exportação de arquivos

**Funções Principais**:

1. `importar_planilha(caminho: str) -> pd.DataFrame`
   - Lê arquivo Excel/CSV
   - Retorna DataFrame do Pandas
   - Suporta: .xlsx, .xls, .csv

2. `exportar_planilha(df: pd.DataFrame, caminho: str, template: Template)`
   - Gera arquivo Excel formatado
   - Aplica estilos do template
   - Salva em disco

**Dependências**: Pandas, OpenPyXL

### SheetProcessor (services/sheet_processor.py)

**Responsabilidade**: Limpar e normalizar planilhas

**Pipeline de Processamento**:

```
Entrada: DataFrame bruto (células mescladas, formatação inconsistente)
    ↓
1. Desmesclar células (preencher valores)
2. Remover linhas/colunas vazias
3. Identificar linha de cabeçalho
4. Padronizar tipos de dados
5. Remover caracteres especiais
    ↓
Saída: DataFrame normalizado e limpo
```

**Funções**:
- `limpar_planilha(df: pd.DataFrame) -> pd.DataFrame`
- `desmesclar_celulas(df: pd.DataFrame) -> pd.DataFrame`
- `identificar_cabecalho(df: pd.DataFrame) -> int`
- `padronizar_tipos(df: pd.DataFrame) -> pd.DataFrame`

### DataMapper (services/data_mapper.py)

**Responsabilidade**: Converter DataFrame em lista de Transactions

**Processo**:

```python
DataFrame (planilha limpa)
    ↓
Para cada linha:
    1. Extrair campos obrigatórios (data, valor, tipo)
    2. Extrair campos extras (demais colunas)
    3. Criar Transaction(data, valor, tipo, **extras)
    4. Validar (Transaction faz validação)
    5. Adicionar à lista ou registrar erro
    ↓
Lista de Transactions válidas + Lista de erros
```

**Funções**:
- `extrair_transactions(df: pd.DataFrame) -> tuple[list[Transaction], list[str]]`
- `identificar_colunas(df: pd.DataFrame) -> dict`
- `classificar_tipo_pagamento(descricao: str) -> str`

### TemplateManager (services/template_manager.py)

**Responsabilidade**: Gerar planilhas formatadas a partir de Transactions

**Processo**:

```
Lista de Transactions + Template
    ↓
1. Criar DataFrame vazio com colunas do template
2. Para cada Transaction:
    - Mapear campos usando template.mapeamento
    - Adicionar linha ao DataFrame
3. Aplicar formatação (cores, estilos)
4. Exportar para Excel
    ↓
Arquivo Excel formatado
```

**Funções**:
- `gerar_planilha(transactions: list[Transaction], template: Template) -> str`
- `aplicar_formatacao(wb: Workbook, template: Template)`
- `carregar_template(nome: str) -> Template`

---

## Interface do Usuário

### Tecnologia: CustomTkinter

**Por que CustomTkinter?**
- Interface moderna e profissional
- Suporte a temas (dark/light)
- Widgets customizáveis
- Compatibilidade com Tkinter tradicional

### Layout da Janela Principal

```
┌─────────────────────────────────────────────────────────────┐
│  [LOGO]  Conciliador Financeiro v2          [⚙️ Config]    │
├──────────────┬────────────────────────┬─────────────────────┤
│              │                        │                     │
│  PAINEL      │    ÁREA CENTRAL        │   HISTÓRICO        │
│  LATERAL     │                        │                     │
│              │  ┌──────────────────┐  │  ┌───────────────┐ │
│  [ Config ]  │  │                  │  │  │ 02/10 10:30   │ │
│  [ Sobre  ]  │  │   [📁 IMPORTAR]  │  │  │ arquivo1.xlsx │ │
│              │  │                  │  │  │ ✅ Sucesso    │ │
│              │  └──────────────────┘  │  ├───────────────┤ │
│              │                        │  │ 01/10 15:45   │ │
│              │  Status: Aguardando... │  │ arquivo2.xlsx │ │
│              │                        │  │ ✅ Sucesso    │ │
│              │                        │  └───────────────┘ │
│              │                        │                     │
└──────────────┴────────────────────────┴─────────────────────┘
```

### Dimensões
- Resolução: 1366x720 (otimizada para laptops)
- Layout: Grid 3 colunas (350px | flex | 450px)

### Tema
- Fundo principal: `#161616` (preto suave)
- Painéis: `#333333` (cinza escuro)
- Botão importar: `#004D40` (verde escuro)
- Botão config: `#810B0B` (vermelho escuro)
- Texto: `#FFFFFF` (branco)

---

## Fluxo de Dados

### Fluxo Completo de Processamento

```
1. USUÁRIO
   ↓ (clica em "Importar")

2. UI (main_window.py)
   ↓ (abre dialog, seleciona arquivo)

3. FileHandler.importar_planilha(caminho)
   ↓ (lê Excel → DataFrame)

4. SheetProcessor.limpar_planilha(df)
   ↓ (normaliza dados)

5. DataMapper.extrair_transactions(df)
   ↓ (cria Transactions, valida)

6. TemplateManager.gerar_planilha(transactions, template)
   ↓ (gera Excel formatado)

7. Database.registrar_historico(...)
   ↓ (salva no SQLite)

8. UI atualiza interface
   ↓ (mostra sucesso/erro)

9. USUÁRIO vê resultado
```

### Fluxo de Validação

```
DataFrame (dados brutos)
    ↓
DataMapper tenta criar Transaction
    ↓
Transaction.__init__ valida dados
    ↓
┌─────────────────┬─────────────────┐
│ Dados válidos?  │ Dados inválidos │
│      SIM        │      NÃO        │
└─────────────────┴─────────────────┘
         ↓                  ↓
  Transaction criada   ValueError lançado
         ↓                  ↓
  Adicionada à lista   Erro registrado
         ↓                  ↓
  Processamento OK    Usuário notificado
```

---

## Guia de Desenvolvimento

### Configuração do Ambiente

**1. Requisitos**:
- Python 3.8+
- pip
- virtualenv (recomendado)

**2. Instalação**:
```bash
# Clonar repositório
git clone <repo-url>
cd conciliador-financeiro

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

**3. Estrutura de Branches**:
```
main                    # Produção (estável)
├── develop/v2         # Desenvolvimento ativo
│   ├── feature/*      # Novas funcionalidades
│   ├── fix/*          # Correções de bugs
│   └── refactor/*     # Refatorações
└── develop/v1         # Código legado (backup)
```

### Fluxo de Trabalho (Workflow)

**1. Criar Nova Funcionalidade**:
```bash
git checkout develop/v2
git pull origin develop/v2
git checkout -b feature/nome-funcionalidade

# Desenvolver...
git add .
git commit -m "feat: descrição da funcionalidade"
git push origin feature/nome-funcionalidade

# Abrir Pull Request para develop/v2
```

**2. Padrão de Commits (Conventional Commits)**:
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `refactor:` - Refatoração sem mudar comportamento
- `docs:` - Documentação
- `test:` - Testes
- `chore:` - Manutenção/build

**Exemplos**:
```bash
git commit -m "feat: adiciona validação de CPF em Transaction"
git commit -m "fix: corrige bug de células mescladas"
git commit -m "refactor: separa lógica de UI em main_window"
git commit -m "docs: atualiza documentação da API"
```

### Ordem de Implementação (Bottom-Up)

**Fase 1 - Fundação (Models)**:
1. `models/transaction.py` ← **COMEÇAR AQUI**
2. `models/template.py`
3. Testar models isoladamente

**Fase 2 - Lógica de Negócio (Services)**:
4. `services/file_handler.py`
5. `services/sheet_processor.py`
6. `services/data_mapper.py`
7. `services/template_manager.py`
8. Testar cada service com models prontos

**Fase 3 - Interface (UI)**:
9. `ui/main_window.py`
10. `ui/styles.py`
11. Integrar com services

**Fase 4 - Persistência**:
12. `database.py`
13. Integração final

### Boas Práticas

**1. Documentação**:
```python
def extrair_transactions(df: pd.DataFrame) -> list[Transaction]:
    """
    Extrai objetos Transaction de um DataFrame.

    Args:
        df: DataFrame limpo e normalizado

    Returns:
        Lista de objetos Transaction válidos

    Raises:
        ValueError: Se DataFrame não tiver colunas obrigatórias
    """
    pass
```

**2. Type Hints**:
```python
from typing import List, Dict, Optional

def processar(arquivo: str) -> Dict[str, any]:
    transactions: List[Transaction] = []
    erros: List[str] = []
    # ...
```

**3. Validações**:
```python
# ❌ Não fazer:
def criar_transaction(valor):
    return Transaction(valor=valor)

# ✅ Fazer:
def criar_transaction(valor: float) -> Transaction:
    if valor <= 0:
        raise ValueError(f"Valor inválido: {valor}")
    return Transaction(valor=valor)
```

**4. Separação de Responsabilidades**:
```python
# ❌ Transaction "inteligente" (faz muita coisa):
class Transaction:
    def salvar_no_banco(self):
        # NÃO!

# ✅ Transaction "burra" (só dados):
class Transaction:
    def to_dict(self) -> dict:
        return {...}
```

---

## API de Referência

### models.transaction.Transaction

```python
class Transaction:
    def __init__(
        self,
        data: Union[str, datetime],
        valor: float,
        tipo_pagamento: str,
        **extras: dict
    ):
        """
        Cria uma transação financeira.

        Args:
            data: Data da transação (str ou datetime)
            valor: Valor monetário (deve ser > 0)
            tipo_pagamento: Método de pagamento
            **extras: Campos adicionais opcionais

        Raises:
            ValueError: Se validação falhar
        """

    def to_dict(self) -> dict:
        """Retorna representação em dicionário"""

    def _validar(self) -> None:
        """Valida dados internos (privado)"""
```

### services.file_handler

```python
def importar_planilha(caminho: str) -> pd.DataFrame:
    """
    Importa planilha Excel/CSV.

    Args:
        caminho: Caminho do arquivo

    Returns:
        DataFrame com dados da planilha

    Raises:
        FileNotFoundError: Se arquivo não existe
        ValueError: Se formato inválido
    """

def exportar_planilha(
    df: pd.DataFrame,
    caminho: str,
    template: Template
) -> str:
    """
    Exporta DataFrame para Excel formatado.

    Args:
        df: DataFrame a exportar
        caminho: Caminho de saída
        template: Template de formatação

    Returns:
        Caminho do arquivo gerado
    """
```

### services.data_mapper

```python
def extrair_transactions(
    df: pd.DataFrame
) -> Tuple[List[Transaction], List[str]]:
    """
    Converte DataFrame em Transactions.

    Args:
        df: DataFrame limpo

    Returns:
        Tupla (lista de Transactions, lista de erros)
    """

def classificar_tipo_pagamento(descricao: str) -> str:
    """
    Identifica tipo de pagamento por descrição.

    Args:
        descricao: Texto descritivo

    Returns:
        Tipo de pagamento (PIX, Cartão, etc.)
    """
```

---

## Exemplos de Uso

### Exemplo 1: Criar Transaction Manualmente

```python
from models.transaction import Transaction
from datetime import datetime

# Criar transação
t = Transaction(
    data=datetime(2025, 10, 2),
    valor=150.50,
    tipo_pagamento="PIX",
    cliente="João Silva",
    nota_fiscal="NF-12345"
)

# Acessar dados
print(t.valor)  # 150.5
print(t.extras['cliente'])  # "João Silva"

# Serializar
dados = t.to_dict()
print(dados)
# {'data': datetime(...), 'valor': 150.5, 'tipo_pagamento': 'PIX', ...}
```

### Exemplo 2: Processar Planilha Completa

```python
from services.file_handler import importar_planilha
from services.sheet_processor import limpar_planilha
from services.data_mapper import extrair_transactions

# 1. Importar
df = importar_planilha("vendas_outubro.xlsx")

# 2. Limpar
df_limpo = limpar_planilha(df)

# 3. Extrair transactions
transactions, erros = extrair_transactions(df_limpo)

print(f"✅ {len(transactions)} transações válidas")
print(f"❌ {len(erros)} erros encontrados")

if erros:
    for erro in erros:
        print(f"  - {erro}")
```

### Exemplo 3: Gerar Planilha Omie

```python
from services.template_manager import gerar_planilha, carregar_template

# Carregar template Omie
template_omie = carregar_template("omie")

# Gerar planilha
arquivo_saida = gerar_planilha(
    transactions=transactions,
    template=template_omie,
    caminho_saida="relatorio_omie_outubro.xlsx"
)

print(f"✅ Planilha gerada: {arquivo_saida}")
```

### Exemplo 4: Validação de Dados

```python
from models.transaction import Transaction

# Tentar criar transação inválida
try:
    t = Transaction(
        data="02/10/2025",
        valor=-100,  # ❌ Valor negativo
        tipo_pagamento="PIX"
    )
except ValueError as e:
    print(f"Erro: {e}")
    # Saída: "Erro: Valor deve ser positivo"
```

---

## Troubleshooting

### Problemas Comuns

#### 1. Erro: "ModuleNotFoundError: No module named 'customtkinter'"

**Causa**: Dependências não instaladas

**Solução**:
```bash
pip install -r requirements.txt
# ou
pip install customtkinter
```

#### 2. Erro: "Células mescladas não processadas"

**Causa**: Planilha com formatação complexa

**Solução**:
```python
# Usar SheetProcessor antes de processar
df_limpo = sheet_processor.desmesclar_celulas(df)
```

#### 3. Erro: "ValueError: Tipo de pagamento inválido"

**Causa**: Tipo não está na lista de aceitos

**Solução**:
```python
# Adicionar tipo em models/transaction.py
TIPOS_VALIDOS = ['PIX', 'Cartão', 'Dinheiro', 'Boleto', 'NOVO_TIPO']
```

#### 4. Interface não abre / Tela preta

**Causa**: Problema com CustomTkinter ou tema

**Solução**:
```bash
# Reinstalar customtkinter
pip uninstall customtkinter
pip install customtkinter --upgrade
```

#### 5. Planilha gerada sem formatação

**Causa**: Template não aplicado corretamente

**Solução**:
```python
# Verificar se template tem atributo 'formatacao'
print(template.formatacao)

# Aplicar manualmente se necessário
template_manager.aplicar_formatacao(workbook, template)
```

### Debug e Logs

**Adicionar logging**:
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='conciliador.log'
)

logger = logging.getLogger(__name__)
logger.debug("Iniciando processamento...")
```

### Performance

**Otimizar processamento de grandes planilhas**:
```python
# Processar em chunks
for chunk in pd.read_excel('grande_arquivo.xlsx', chunksize=1000):
    transactions, erros = extrair_transactions(chunk)
    # processar...
```

---

## Roadmap

### v2.0.0 (Atual - Em Desenvolvimento)
- [x] Refatoração completa da arquitetura
- [x] Separação Models/Services/UI
- [ ] Sistema de validação robusto
- [ ] Múltiplos templates
- [ ] Interface modernizada

### v2.1.0 (Planejado)
- [ ] Suporte a CSV
- [ ] Exportação para PDF
- [ ] Relatórios estatísticos
- [ ] Configurações por template

### v2.2.0 (Futuro)
- [ ] API REST
- [ ] Dashboard web
- [ ] Integração com APIs bancárias
- [ ] Machine Learning para classificação

---

## Referências

### Bibliotecas Utilizadas

- [Pandas](https://pandas.pydata.org/docs/) - Manipulação de dados
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Processamento Excel
- [CustomTkinter](https://customtkinter.tomschimansky.com/) - Interface gráfica
- [SQLite](https://www.sqlite.org/docs.html) - Banco de dados

### Padrões e Convenções

- [PEP 8](https://peps.python.org/pep-0008/) - Style Guide Python
- [Conventional Commits](https://www.conventionalcommits.org/) - Padrão de commits
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID) - Princípios de design

---

**Última atualização**: 02/10/2025
**Versão da documentação**: 2.0.0
