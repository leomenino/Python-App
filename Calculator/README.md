# Calculator App

Calculadora com interface gráfica construída em Python usando PyQt5, com botões numéricos, operações básicas, suporte a teclado físico e um parser seguro de expressões.

## 🖼️ Funcionalidades

- Interface gráfica com teclado numérico (0-9) e operadores (+, -, *, /)
- Botão **Clear** para limpar o campo de entrada
- Botão **<** para apagar o último carácter introduzido
- Cálculo do resultado ao pressionar **=**
- **Suporte a teclado físico**: números, operadores, `Enter` (calcular), `Backspace` (apagar) e `Esc` (limpar)
- **Erros visíveis na interface** (ex: `Erro: Divisão por zero`), em vez de só no terminal
- Estilo personalizado (fundo escuro, fonte Comic Sans nos botões)

## 🔒 Segurança

O cálculo das expressões não usa `eval()`. Em vez disso, usa um parser próprio (`safe_eval`) baseado no módulo `ast` do Python, que só permite números e os operadores `+ - * /`. Isto evita que a aplicação execute código arbitrário através do campo de texto.

## 🛠️ Tecnologias

- Python 3
- PyQt5
- `ast` (parsing seguro de expressões)

## 📦 Instalação

Instala a dependência necessária:

```bash
pip install PyQt5
```

## 🚀 Como correr

```bash
python3 calculator.py
```

## 💡 Como funciona

- Cada botão (e cada tecla do teclado) chama `process_input()`, que atualiza o campo de texto
- Ao pressionar `=` ou `Enter`, a expressão é validada e calculada por `safe_eval()`
- Erros de sintaxe, divisão por zero ou operações não permitidas são apanhados e mostrados diretamente na interface

## 📌 Possíveis melhorias futuras

- Suporte a mais operações (percentagem, raiz quadrada, potências)
- Histórico de cálculos anteriores
- Testes automatizados para `safe_eval()`
