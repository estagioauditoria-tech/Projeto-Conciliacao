# 🗺️ Fluxograma Completo - Conciliador Financeiro v2

> Visualização do fluxo de dados do início ao fim do sistema

**Autor**: Paulo Ygor - Estagiário | Grupo Doma
**Data**: 02/10/2025

---

## 📋 Como visualizar este fluxograma

### No VS Code:
1. Instale a extensão **Markdown Preview Mermaid Support**
   - ID: `bierner.markdown-mermaid`
2. Abra este arquivo
3. Pressione `Ctrl+Shift+V` (ou `Cmd+Shift+V` no Mac)
4. O diagrama será renderizado automaticamente

### Online (alternativa):
- Copie o código Mermaid e cole em: https://mermaid.live/

---

## 🌊 FLUXO PRINCIPAL: DO USUÁRIO AO RESULTADO

```mermaid
graph TD
    A[👤 USUÁRIO<br/>Clica em 'Importar'] --> B[🖥️ UI - main_window.py<br/>Abre diálogo de arquivo]
    B --> C{Arquivo<br/>selecionado?}
    C -->|NÃO| A
    C -->|SIM| D[📂 FileHandler.ler_planilha<br/>Lê arquivo Excel]

    D --> E{Arquivo<br/>válido?}
    E -->|NÃO| F[❌ UI mostra erro<br/>Arquivo corrompido/inválido]
    F --> A

    E -->|SIM| G[📊 DataFrame BRUTO<br/>com células mescladas, sujeira]
    G --> H[🧹 SheetProcessor.limpar_planilha<br/>Desmescla, remove vazios]
    H --> I[📊 DataFrame LIMPO<br/>normalizado, pronto]

    I --> J[🔄 DataMapper.extrair_transactions<br/>Converte linhas em Transaction]
    J --> K{Validação<br/>Transaction}

    K -->|VÁLIDA| L[✅ Lista de Transactions<br/>dados validados]
    K -->|INVÁLIDA| M[📝 Lista de Erros<br/>registra problema]

    L --> N[📑 TemplateManager.gerar_planilha<br/>Aplica template Omie]
    M --> N

    N --> O[💾 FileHandler.escrever_planilha<br/>Salva Excel formatado]
    O --> P[🗄️ Database.registrar_historico<br/>Salva operação no SQLite]

    P --> Q[✅ UI atualiza interface<br/>Mostra sucesso + estatísticas]
    Q --> R[👤 USUÁRIO<br/>Vê resultado e pode baixar arquivo]

    style A fill:#4CAF50,stroke:#2E7D32,color:#fff
    style R fill:#4CAF50,stroke:#2E7D32,color:#fff
    style F fill:#F44336,stroke:#C62828,color:#fff
    style M fill:#FF9800,stroke:#F57C00,color:#fff
    style L fill:#2196F3,stroke:#1565C0,color:#fff
    style O fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 🏗️ ARQUITETURA EM CAMADAS

```mermaid
graph TB
    subgraph "🖥️ CAMADA DE APRESENTAÇÃO (UI)"
        UI1[main_window.py<br/>Interface gráfica]
        UI2[styles.py<br/>Temas e cores]
    end

    subgraph "⚙️ CAMADA DE SERVIÇOS (Business Logic)"
        S1[file_handler.py<br/>Lê/Escreve Excel]
        S2[sheet_processor.py<br/>Limpa dados]
        S3[data_mapper.py<br/>Mapeia p/ Transaction]
        S4[template_manager.py<br/>Gera planilhas formatadas]
    end

    subgraph "📦 CAMADA DE MODELOS (Data)"
        M1[transaction.py<br/>Dados + Validação]
        M2[template.py<br/>Estrutura de templates]
    end

    subgraph "🗄️ CAMADA DE PERSISTÊNCIA"
        DB[(database.py<br/>SQLite - Histórico)]
    end

    UI1 --> S1
    UI1 --> S4
    S1 --> S2
    S2 --> S3
    S3 --> M1
    S4 --> M1
    S4 --> M2
    UI1 --> DB

    style UI1 fill:#673AB7,stroke:#4527A0,color:#fff
    style S1 fill:#2196F3,stroke:#1565C0,color:#fff
    style S2 fill:#2196F3,stroke:#1565C0,color:#fff
    style S3 fill:#2196F3,stroke:#1565C0,color:#fff
    style S4 fill:#2196F3,stroke:#1565C0,color:#fff
    style M1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style M2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style DB fill:#FF9800,stroke:#F57C00,color:#fff
```

---

## 📂 FILEHANDLER: LEITURA DE ARQUIVO

```mermaid
graph TD
    A[ler_planilha caminho] --> B{Arquivo<br/>existe?}
    B -->|NÃO| C[❌ FileNotFoundError<br/>Arquivo não encontrado]

    B -->|SIM| D{Extensão<br/>válida?}
    D -->|NÃO .xlsx/.xls| E[❌ ValueError<br/>Formato inválido]

    D -->|SIM| F[pd.read_excel caminho]
    F --> G{Leitura<br/>ok?}

    G -->|ERRO| H[❌ Exception<br/>Arquivo corrompido ou sem permissão]
    G -->|OK| I[✅ Retorna DataFrame BRUTO<br/>Com células mescladas, formatação, sujeira]

    style A fill:#2196F3,stroke:#1565C0,color:#fff
    style I fill:#4CAF50,stroke:#2E7D32,color:#fff
    style C fill:#F44336,stroke:#C62828,color:#fff
    style E fill:#F44336,stroke:#C62828,color:#fff
    style H fill:#F44336,stroke:#C62828,color:#fff
```

### 📝 Responsabilidade:
- ✅ Verificar se arquivo existe
- ✅ Validar extensão (.xlsx, .xls)
- ✅ Ler com pandas
- ✅ Tratar erros (arquivo corrompido, sem permissão)
- ❌ NÃO limpa dados (isso é SheetProcessor)
- ❌ NÃO valida conteúdo (isso é DataMapper)

---

## 🧹 SHEETPROCESSOR: LIMPEZA DE DADOS

```mermaid
graph TD
    A[limpar_planilha df_bruto] --> B[Identificar células mescladas<br/>NaN consecutivos na mesma coluna]
    B --> C[Propagar valores<br/>Preencher NaN com valor da célula de cima]
    C --> D[Remover linhas totalmente vazias<br/>dropna how='all']
    D --> E[Remover colunas totalmente vazias<br/>dropna axis=1 how='all']
    E --> F[Identificar linha de cabeçalho<br/>Primeira linha com texto válido]
    F --> G[Padronizar tipos de dados<br/>Números como float, datas como datetime]
    G --> H[Remover caracteres especiais<br/>R$, %, espaços extras]
    H --> I[✅ Retorna DataFrame LIMPO<br/>Normalizado, pronto para mapear]

    style A fill:#2196F3,stroke:#1565C0,color:#fff
    style I fill:#4CAF50,stroke:#2E7D32,color:#fff
```

### 📝 Responsabilidade:
- ✅ Desmesclar células (propagar valores)
- ✅ Remover linhas/colunas vazias
- ✅ Identificar cabeçalho automaticamente
- ✅ Normalizar tipos (números, datas)
- ✅ Remover formatação decorativa
- ❌ NÃO valida regras de negócio (isso é Transaction)
- ❌ NÃO cria objetos (isso é DataMapper)

---

## 🔄 DATAMAPPER: CONVERSÃO PARA TRANSACTION

```mermaid
graph TD
    A[extrair_transactions df_limpo] --> B[Identificar colunas obrigatórias<br/>data, valor, tipo_pagamento]
    B --> C{Colunas<br/>encontradas?}
    C -->|NÃO| D[❌ ValueError<br/>Planilha não tem colunas necessárias]

    C -->|SIM| E[Para cada linha do DataFrame]
    E --> F[Extrair campos obrigatórios<br/>data, valor, tipo]
    F --> G[Extrair campos extras<br/>demais colunas → dict]

    G --> H[Tentar criar Transaction<br/>data, valor, tipo, **extras]
    H --> I{Transaction<br/>válida?}

    I -->|SIM| J[Adiciona à lista_sucesso]
    I -->|NÃO| K[Captura ValueError<br/>Adiciona à lista_erros]

    J --> L{Mais<br/>linhas?}
    K --> L
    L -->|SIM| E
    L -->|NÃO| M[✅ Retorna lista_sucesso, lista_erros]

    style A fill:#2196F3,stroke:#1565C0,color:#fff
    style M fill:#4CAF50,stroke:#2E7D32,color:#fff
    style D fill:#F44336,stroke:#C62828,color:#fff
    style K fill:#FF9800,stroke:#F57C00,color:#fff
```

### 📝 Responsabilidade:
- ✅ Identificar colunas automaticamente
- ✅ Mapear linhas do DataFrame → Transaction
- ✅ Capturar erros de validação
- ✅ Retornar lista de sucessos + lista de erros
- ❌ NÃO valida dados (isso é Transaction)
- ❌ NÃO limpa planilha (isso é SheetProcessor)

---

## ✅ TRANSACTION: VALIDAÇÃO DE DADOS

```mermaid
graph TD
    A[Transaction __init__<br/>data, valor, tipo, **extras] --> B[Validar valor > 0]
    B --> C{Valor<br/>positivo?}
    C -->|NÃO| D[❌ raise ValueError<br/>Valor deve ser positivo]

    C -->|SIM| E[Validar tipo in TIPOS_VALIDOS]
    E --> F{Tipo<br/>válido?}
    F -->|NÃO| G[❌ raise ValueError<br/>Tipo de pagamento inválido]

    F -->|SIM| H[Validar data not empty]
    H --> I{Data<br/>preenchida?}
    I -->|NÃO| J[❌ raise ValueError<br/>Data não pode ser vazia]

    I -->|SIM| K[Guardar atributos<br/>self.data, self.valor, self.tipo]
    K --> L[Guardar extras<br/>self.extras = extras]
    L --> M[✅ Transaction criada<br/>Objeto válido]

    style A fill:#2196F3,stroke:#1565C0,color:#fff
    style M fill:#4CAF50,stroke:#2E7D32,color:#fff
    style D fill:#F44336,stroke:#C62828,color:#fff
    style G fill:#F44336,stroke:#C62828,color:#fff
    style J fill:#F44336,stroke:#C62828,color:#fff
```

### 📝 Responsabilidade:
- ✅ Armazenar dados (data, valor, tipo, extras)
- ✅ Validar regras básicas (valor > 0, tipo válido)
- ✅ Disparar erro se inválido (raise ValueError)
- ✅ Serializar para dict (to_dict)
- ❌ NÃO lê planilhas (isso é FileHandler)
- ❌ NÃO processa dados (isso é SheetProcessor)
- ❌ NÃO busca dados (isso é DataMapper)

---

## 📑 TEMPLATEMANAGER: GERAÇÃO DE PLANILHA FORMATADA

```mermaid
graph TD
    A[gerar_planilha<br/>transactions, template] --> B[Criar DataFrame vazio<br/>com colunas do template]
    B --> C[Para cada Transaction]
    C --> D[Aplicar mapeamento<br/>transaction.data → coluna 'Data']
    D --> E[Adicionar linha ao DataFrame]
    E --> F{Mais<br/>transactions?}
    F -->|SIM| C

    F -->|NÃO| G[Criar arquivo Excel<br/>openpyxl Workbook]
    G --> H[Aplicar formatação<br/>cores, bordas, larguras]
    H --> I[Salvar arquivo<br/>caminho_saida.xlsx]
    I --> J[✅ Retorna caminho do arquivo gerado]

    style A fill:#2196F3,stroke:#1565C0,color:#fff
    style J fill:#4CAF50,stroke:#2E7D32,color:#fff
```

### 📝 Responsabilidade:
- ✅ Converter lista de Transaction → DataFrame
- ✅ Aplicar mapeamento do template
- ✅ Aplicar formatação (cores, bordas)
- ✅ Gerar arquivo Excel formatado
- ❌ NÃO valida dados (isso é Transaction)
- ❌ NÃO lê arquivos (isso é FileHandler)

---

## 🔀 FLUXO DE VALIDAÇÃO (DETALHE)

```mermaid
graph TD
    A[DataFrame limpo<br/>linhas prontas] --> B[DataMapper itera linha por linha]
    B --> C[Tenta criar Transaction<br/>data, valor, tipo, **extras]
    C --> D[Transaction.__init__<br/>executa validações]

    D --> E{Dados<br/>válidos?}
    E -->|SIM| F[✅ Transaction criada<br/>Objeto válido na memória]
    E -->|NÃO| G[❌ raise ValueError<br/>Validação falhou]

    F --> H[DataMapper adiciona à<br/>lista_sucesso]
    G --> I[DataMapper captura erro<br/>try/except ValueError]
    I --> J[Adiciona mensagem à<br/>lista_erros]

    H --> K{Mais<br/>linhas?}
    J --> K
    K -->|SIM| B
    K -->|NÃO| L[Retorna<br/>lista_sucesso, lista_erros]

    L --> M[UI mostra estatísticas<br/>X sucessos, Y erros]

    style F fill:#4CAF50,stroke:#2E7D32,color:#fff
    style G fill:#F44336,stroke:#C62828,color:#fff
    style J fill:#FF9800,stroke:#F57C00,color:#fff
    style M fill:#673AB7,stroke:#4527A0,color:#fff
```

---

## 🎯 QUEM FAZ O QUÊ? (RESUMO)

```mermaid
graph LR
    subgraph "📂 FileHandler"
        FH1[Lê Excel → DataFrame]
        FH2[Escreve DataFrame → Excel]
    end

    subgraph "🧹 SheetProcessor"
        SP1[Desmescla células]
        SP2[Remove vazios]
        SP3[Normaliza tipos]
    end

    subgraph "🔄 DataMapper"
        DM1[Identifica colunas]
        DM2[Mapeia linhas → Transaction]
        DM3[Captura erros]
    end

    subgraph "✅ Transaction"
        T1[Armazena dados]
        T2[Valida regras]
        T3[Dispara erros]
    end

    subgraph "📑 TemplateManager"
        TM1[Converte Transaction → Excel]
        TM2[Aplica formatação]
    end

    style FH1 fill:#2196F3,stroke:#1565C0,color:#fff
    style FH2 fill:#2196F3,stroke:#1565C0,color:#fff
    style SP1 fill:#00BCD4,stroke:#0097A7,color:#fff
    style SP2 fill:#00BCD4,stroke:#0097A7,color:#fff
    style SP3 fill:#00BCD4,stroke:#0097A7,color:#fff
    style DM1 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style DM2 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style DM3 fill:#4CAF50,stroke:#2E7D32,color:#fff
    style T1 fill:#FF9800,stroke:#F57C00,color:#fff
    style T2 fill:#FF9800,stroke:#F57C00,color:#fff
    style T3 fill:#FF9800,stroke:#F57C00,color:#fff
    style TM1 fill:#9C27B0,stroke:#6A1B9A,color:#fff
    style TM2 fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

---

## 📊 EXEMPLO CONCRETO: PROCESSAR "vendas_outubro.xlsx"

```mermaid
sequenceDiagram
    participant U as 👤 Usuário
    participant UI as 🖥️ UI
    participant FH as 📂 FileHandler
    participant SP as 🧹 SheetProcessor
    participant DM as 🔄 DataMapper
    participant T as ✅ Transaction
    participant TM as 📑 TemplateManager
    participant DB as 🗄️ Database

    U->>UI: Clica "Importar"
    UI->>U: Abre diálogo
    U->>UI: Seleciona "vendas_outubro.xlsx"

    UI->>FH: ler_planilha("vendas_outubro.xlsx")
    FH->>FH: Valida arquivo existe
    FH->>FH: pd.read_excel()
    FH-->>UI: DataFrame BRUTO (100 linhas, células mescladas)

    UI->>SP: limpar_planilha(df_bruto)
    SP->>SP: Desmescla células
    SP->>SP: Remove vazios
    SP->>SP: Normaliza tipos
    SP-->>UI: DataFrame LIMPO (95 linhas úteis)

    UI->>DM: extrair_transactions(df_limpo)
    DM->>DM: Identifica colunas
    loop Para cada linha
        DM->>T: Transaction(data, valor, tipo, **extras)
        alt Dados válidos
            T-->>DM: ✅ Transaction criada
            DM->>DM: Adiciona à lista_sucesso
        else Dados inválidos
            T-->>DM: ❌ ValueError
            DM->>DM: Adiciona à lista_erros
        end
    end
    DM-->>UI: 90 sucessos, 5 erros

    UI->>TM: gerar_planilha(transactions, template_omie)
    TM->>TM: Converte Transaction → DataFrame
    TM->>TM: Aplica formatação
    TM->>FH: escrever_planilha(df, "relatorio_omie.xlsx")
    FH-->>TM: ✅ Arquivo salvo
    TM-->>UI: "relatorio_omie.xlsx"

    UI->>DB: registrar_historico(...)
    DB-->>UI: ✅ Salvo no SQLite

    UI->>U: Mostra: 90 transações, 5 erros, arquivo gerado
```

---

## 🧠 PRINCÍPIOS ARQUITETURAIS

### 1️⃣ Separação de Responsabilidades (SRP)

```mermaid
graph TD
    A[Transaction] --> A1[Armazenar<br/>Validar]
    B[FileHandler] --> B1[Ler<br/>Escrever]
    C[SheetProcessor] --> C1[Limpar<br/>Normalizar]
    D[DataMapper] --> D1[Mapear<br/>Transformar]
    E[TemplateManager] --> E1[Formatar<br/>Gerar]

    style A fill:#4CAF50,stroke:#2E7D32,color:#fff
    style B fill:#2196F3,stroke:#1565C0,color:#fff
    style C fill:#00BCD4,stroke:#0097A7,color:#fff
    style D fill:#FF9800,stroke:#F57C00,color:#fff
    style E fill:#9C27B0,stroke:#6A1B9A,color:#fff
```

**Regra de ouro**: Cada módulo faz UMA coisa e faz BEM.

### 2️⃣ Bottom-Up (Menos → Mais Dependências)

```mermaid
graph BT
    UI[UI<br/>Depende de TUDO] --> TM[TemplateManager]
    UI --> FH[FileHandler]
    TM --> T[Transaction]
    FH --> SP[SheetProcessor]
    SP --> DM[DataMapper]
    DM --> T
    T --> NADA[❌ Não depende de NADA]

    style T fill:#4CAF50,stroke:#2E7D32,color:#fff
    style NADA fill:#F44336,stroke:#C62828,color:#fff
```

**Ordem de desenvolvimento**:
1. Transaction (zero dependências)
2. Template (zero dependências)
3. FileHandler → SheetProcessor → DataMapper (dependem de Transaction)
4. TemplateManager (depende de Transaction + Template)
5. UI (depende de tudo)

### 3️⃣ Classes "Burras" vs "Inteligentes"

```mermaid
graph LR
    subgraph "🐑 BURRAS (só dados)"
        B1[Transaction<br/>Guarda: data, valor, tipo]
        B2[Template<br/>Guarda: colunas, mapeamento]
    end

    subgraph "🧠 INTELIGENTES (lógica)"
        I1[SheetProcessor<br/>Processa planilhas]
        I2[DataMapper<br/>Transforma dados]
        I3[TemplateManager<br/>Gera relatórios]
    end

    I1 --> B1
    I2 --> B1
    I3 --> B1
    I3 --> B2

    style B1 fill:#FFE082,stroke:#F57F17,color:#000
    style B2 fill:#FFE082,stroke:#F57F17,color:#000
    style I1 fill:#81C784,stroke:#2E7D32,color:#fff
    style I2 fill:#81C784,stroke:#2E7D32,color:#fff
    style I3 fill:#81C784,stroke:#2E7D32,color:#fff
```

---

## ✅ CHECKLIST DE DESENVOLVIMENTO

### Fase 1: Models
- [x] Transaction.py (FEITO ✅)
- [ ] Template.py

### Fase 2: Services
- [ ] FileHandler.py ← **PRÓXIMO**
- [ ] SheetProcessor.py
- [ ] DataMapper.py
- [ ] TemplateManager.py

### Fase 3: UI
- [ ] main_window.py (integração)
- [ ] styles.py

### Fase 4: Persistência
- [ ] database.py

---

**Última atualização**: 02/10/2025
**Versão**: 2.0.0
