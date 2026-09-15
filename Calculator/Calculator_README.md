# Calculator App

Calculadora com interface gráfica construída em Python usando PyQt5, com botões numéricos, operações básicas e um design personalizado.

## 🖼️ Funcionalidades

- Interface gráfica com teclado numérico (0-9) e operadores (+, -, *, /)
- Botão **Clear** para limpar o campo de entrada
- Botão **<** para apagar o último carácter introduzido
- Cálculo do resultado ao pressionar **=**
- Estilo personalizado (fundo escuro, fonte Comic Sans nos botões)

## 🛠️ Tecnologias

- Python 3
- PyQt5

## 📦 Instalação

Instala a dependência necessária:

```bash
pip install PyQt5
```

## 🚀 Como correr

```bash
python3 calculator.py
```

*(substitui `calculator.py` pelo nome real do ficheiro principal)*

## 💡 Como funciona

Cada botão está ligado à função `button_click`, que:
- Adiciona o carácter clicado ao campo de texto
- Avalia a expressão matemática com `eval()` quando se pressiona `=`
- Limpa ou apaga carácteres consoante o botão **Clear** ou **<**

## 📌 Possíveis melhorias futuras

- Substituir `eval()` por um parser mais seguro (evitar riscos de segurança com input do utilizador)
- Adicionar suporte para teclado físico
- Tratamento de erros mais visível na interface (em vez de só no terminal)
