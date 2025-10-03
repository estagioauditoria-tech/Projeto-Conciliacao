# Features Futuras - Conciliador Financeiro V2

Este documento registra melhorias e funcionalidades identificadas durante o desenvolvimento do MVP que serão implementadas em versões futuras.

---

## 1. Configuração: Incluir Valores Negativos

**Status:** Identificado
**Prioridade:** Média
**Módulo:** DataMapper (`data_mapper.py`)

### Descrição
Atualmente, a validação do Transaction rejeita valores negativos. Em alguns cenários, planilhas contêm valores negativos representando saídas/despesas.

### Problema Identificado
- **Local:** `extract_transactions()` em `data_mapper.py`
- **Erro:** "O valor não pode ser negativo."
- **Ocorrência:** 1 transação falhou (linha 94) de 95 totais durante testes

### Solução Proposta
Adicionar parâmetro de configuração `incluir_negativos` na função `extract_transactions()`:

```python
def extract_transactions(df, incluir_negativos=False):
    # ...
    valor = row[mapping["valor"]]

    # Tratamento de valores negativos
    if valor < 0:
        if not incluir_negativos:
            continue  # Pula esta linha
        else:
            valor = abs(valor)  # Converte para positivo
            extras['tipo_movimento'] = 'saída'
    else:
        extras['tipo_movimento'] = 'entrada'

    # ... resto do código
```

### Integração com UI
Na interface futura, o usuário poderá escolher:
- **Opção 1:** "Apenas entradas" (padrão, `incluir_negativos=False`)
- **Opção 2:** "Com entradas e saídas" (`incluir_negativos=True`)

### Benefícios
- Flexibilidade para diferentes tipos de relatórios
- Não quebra validação existente (valores sempre positivos no Transaction)
- Adiciona metadado `tipo_movimento` para análise posterior

---

## 2. Template Manager

**Status:** Planejado
**Prioridade:** Alta
**Módulo:** A definir

### Descrição
Sistema para salvar e reutilizar mapeamentos de colunas personalizados.

### Funcionalidades
- Salvar mapeamento de colunas bem-sucedido como template
- Listar templates disponíveis
- Aplicar template específico em nova importação
- Editar/deletar templates existentes

---

## 3. Validações Adicionais

**Status:** Identificado
**Prioridade:** Baixa
**Módulo:** SheetProcessor

### Melhorias Propostas
- Detecção de datas em múltiplos formatos (DD/MM/YYYY, YYYY-MM-DD, etc.)
- Validação de intervalo de datas (alertar se data muito antiga/futura)
- Detecção automática de encoding para arquivos CSV

---

## 4. Relatórios e Estatísticas

**Status:** Planejado
**Prioridade:** Média
**Módulo:** A definir

### Funcionalidades
- Resumo de importação (total de linhas, sucessos, erros)
- Estatísticas por tipo de pagamento
- Gráficos de distribuição temporal
- Exportação de relatórios de erros

---

## Como Usar Este Documento

1. **Durante o desenvolvimento:** Adicione novas features identificadas aqui
2. **Pós-MVP:** Priorize e implemente features conforme necessidade
3. **Versionamento:** Mova features implementadas para CHANGELOG.md

---

**Última atualização:** 03/10/2025
**Autor:** Paulo Ygor - Estagiário | Grupo Doma
