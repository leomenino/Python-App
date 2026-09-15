# Controlo de Despesas

Aplicação de desktop para registar, filtrar, analisar e exportar despesas pessoais, com interface gráfica em PyQt5 e persistência de dados numa base de dados SQLite.

## 🖼️ Funcionalidades

- Registo de despesas com data, categoria, montante e descrição
- Validação do montante (tem de ser um número válido e maior que zero)
- Categorias pré-definidas (Alimentação, Transporte, Aluguer, Compras, Entretenimento, Contas, Outros)
- **Filtros** por categoria e por intervalo de datas
- **Totais automáticos**: total geral (segundo o filtro aplicado) e resumo do mês atual
- **Exportação para CSV**, respeitando os filtros ativos
- Eliminação de despesas selecionadas, com confirmação antes de apagar
- Botão para limpar os campos do formulário e outro para limpar os filtros
- Tabela só de leitura, com linhas alternadas e seleção por linha completa
- Interface em português, com estilo visual personalizado (cores, cantos arredondados, estados de foco/hover)

## 🛠️ Tecnologias

- Python 3
- PyQt5 (`QtWidgets`, `QtSql`)
- SQLite (via `QSqlDatabase` / `QSqlQuery`)
- `csv` e `pathlib` (exportação de dados)

## 🗄️ Base de dados

Os dados são guardados localmente em `expense.db` (na mesma pasta do script), numa tabela `expenses` criada automaticamente na primeira execução:

```sql
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
```

Todas as queries (inserir, listar, filtrar, apagar) usam **parâmetros preparados** (`query.prepare()` + `addBindValue()`), evitando SQL injection. Os filtros por categoria e intervalo de datas são aplicados diretamente na cláusula `WHERE` da query, em vez de filtrar em Python — reduz a quantidade de dados transferidos e aproveita os índices da base de dados.

## 📦 Instalação

```bash
pip install PyQt5
```

## 🚀 Como correr

```bash
python3 expense_tracker.py
```

*(substitui `expense_tracker.py` pelo nome real do ficheiro principal)*

Na primeira execução, o ficheiro `expense.db` é criado automaticamente na mesma pasta do script.

## 💡 Como funciona

- **Adicionar despesa**: preenche data, categoria, montante e descrição, e clica em "Adicionar". O montante é validado antes de ser guardado na base de dados.
- **Filtrar**: escolhe uma categoria e/ou um intervalo de datas, e clica em "Aplicar filtro". A tabela e os totais atualizam-se de acordo com o filtro. "Limpar filtro" repõe a vista completa.
- **Totais**: o total geral e o resumo do mês atual são recalculados automaticamente sempre que a tabela é carregada.
- **Exportar CSV**: gera um ficheiro `expenses_export.csv` na pasta `Saved/`, com os dados que correspondem ao filtro ativo no momento.
- **Eliminar despesa**: seleciona uma linha na tabela e clica em "Eliminar" — pede confirmação antes de remover o registo.

## 📌 Possíveis melhorias futuras

- Edição de despesas já registadas (atualmente só é possível adicionar e eliminar)
- Gráficos de gastos por categoria/mês (ex: com Matplotlib)
- Testes automatizados para a lógica de filtros e exportação
- Suporte a múltiplas moedas
