#Imports
import ast
import operator

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtCore import Qt


# Operadores permitidos para o parser seguro (substitui o eval())
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,  # números negativos, ex: -5
}


def safe_eval(expression):
    """
    Avalia expressões matemáticas simples (+, -, *, /) sem os riscos do eval().
    Lança ValueError se a expressão for inválida ou usar algo não permitido.
    """
    try:
        node = ast.parse(expression, mode="eval").body
    except SyntaxError:
        raise ValueError("Expressão inválida")

    def _evaluate(node):
        if isinstance(node, ast.Constant):  # números
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Valor inválido")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Operação não permitida")
            left = _evaluate(node.left)
            right = _evaluate(node.right)
            if op_type is ast.Div and right == 0:
                raise ValueError("Divisão por zero")
            return ALLOWED_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Operação não permitida")
            return ALLOWED_OPERATORS[op_type](_evaluate(node.operand))
        else:
            raise ValueError("Expressão não permitida")

    return _evaluate(node)


class CalcApp(QWidget):
    def __init__(self):
        super().__init__()

        # App Settings
        self.setWindowTitle("Calculator App")
        self.resize(250, 300)

        # Create all widgets
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))
        self.text_box.setAlignment(Qt.AlignRight)
        # Permite continuar a escrever com o teclado, mas o foco fica sempre disponível
        self.text_box.setReadOnly(False)

        self.grid = QGridLayout()

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]
        row = 0
        col = 0

        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_click)
            button.setStyleSheet("QPushButton { font: 25pt Comic Sans; padding: 10px; }")
            self.grid.addWidget(button, row, col)
            col += 1

            if col > 3:
                col = 0
                row += 1

        self.clear = QPushButton("Clear")
        self.delete = QPushButton("<")
        self.clear.setStyleSheet("QPushButton { font: 25pt Comic Sans MS; padding: 10px; }")
        self.delete.setStyleSheet("QPushButton { font: 25pt Comic Sans MS; padding: 10px; }")

        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)
        master_layout.addLayout(button_row)
        master_layout.setContentsMargins(25, 25, 25, 25)

        self.setLayout(master_layout)

        self.clear.clicked.connect(self.button_click)
        self.delete.clicked.connect(self.button_click)

    def button_click(self):
        button = self.sender()
        text = button.text()
        self.process_input(text)

    def process_input(self, text):
        """Trata um 'input' vindo tanto dos botões como do teclado físico."""
        if text == "=":
            self.calculate()
        elif text == "Clear":
            self.text_box.clear()
        elif text == "<":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)

    def calculate(self):
        expression = self.text_box.text()
        try:
            result = safe_eval(expression)
            self.text_box.setText(str(result))
        except (ValueError, ZeroDivisionError) as e:
            # Erro visível na interface, não só no terminal
            self.text_box.setText("Erro: " + str(e))
        except Exception:
            self.text_box.setText("Erro: expressão inválida")

    def keyPressEvent(self, event: QKeyEvent):
        """Suporte para teclado físico: números, operadores, Enter, Backspace, Esc."""
        key = event.key()
        text = event.text()

        if key in (Qt.Key_Enter, Qt.Key_Return):
            self.calculate()
        elif key == Qt.Key_Backspace:
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        elif key == Qt.Key_Escape:
            self.text_box.clear()
        elif text in "0123456789.+-*/":
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    main_window = CalcApp()
    main_window.setStyleSheet("QWidget { background-color: #333333}")
    main_window.show()
    app.exec_()
