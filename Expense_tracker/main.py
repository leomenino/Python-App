# Import Modules
import csv
import sys
from pathlib import Path

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
SAVED_DIR = ROOT_DIR / "Saved"


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(550, 500)
        self.setWindowTitle("Controlo de Despesas")

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.filter_dropdown = QComboBox()
        self.filter_start_date = QDateEdit()
        self.filter_end_date = QDateEdit()
        self.filter_start_date.setDate(QDate(2000, 1, 1))
        self.filter_end_date.setDate(QDate.currentDate())
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Ex: 45.90")
        self.description = QLineEdit()
        self.description.setPlaceholderText("Ex: Mercado")

        self.add_button = QPushButton("Adicionar")
        self.clear_button = QPushButton("Limpar")
        self.delete_button = QPushButton("Eliminar")
        self.export_button = QPushButton("Exportar CSV")
        self.apply_filter_button = QPushButton("Aplicar filtro")
        self.clear_filter_button = QPushButton("Limpar filtro")
        self.add_button.clicked.connect(self.add_expense)
        self.clear_button.clicked.connect(self.clear_fields)
        self.delete_button.clicked.connect(self.delete_expense)
        self.export_button.clicked.connect(self.export_csv)
        self.apply_filter_button.clicked.connect(self.load_table)
        self.clear_filter_button.clicked.connect(self.reset_filters)

        self.table = QTableWidget()
        self.table.setColumnCount(5) #Id,date,category,amount,description
        self.table.setHorizontalHeaderLabels(["Id","Data","Categoria","Montante","Descrição"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1, Qt.DescendingOrder)


  


    #Design app with layouts
        
        self.dropdown.addItems(["Alimentação","Transporte","Aluguer","Compras","Entretenimento","Contas","Outros"])
        self.filter_dropdown.addItem("Todas")
        self.filter_dropdown.addItems(["Alimentação","Transporte","Aluguer","Compras","Entretenimento","Contas","Outros"])
        self.filter_dropdown.currentIndexChanged.connect(self.load_table)

        self.total_label = QLabel("Total: € 0.00")
        self.total_label.setAlignment(Qt.AlignRight)
        self.monthly_summary_label = QLabel("Resumo deste mês: € 0.00")
        self.monthly_summary_label.setAlignment(Qt.AlignRight)

        self.setStyleSheet("""
                            QWidget{
                                background-color: #edf3ff;
                                color: #1f2a37;
                                font-family: 'Segoe UI';
                            }

                            QLabel{
                                color: #1f2a37;
                                font-size: 14px;
                                font-weight: 600;
                            }

                            QLineEdit, QComboBox, QDateEdit{
                                background-color: #ffffff;
                                color: #1f2a37;
                                border: 1px solid #b7c7e6;
                                border-radius: 6px;
                                padding: 8px 10px;
                            }

                            QLineEdit:focus, QComboBox:focus, QDateEdit:focus{
                                border: 2px solid #5b8def;
                            }

                           QTableWidget{
                                background-color: #ffffff;
                                color:#1f2a37;
                                border: 1px solid #c9d7f3;
                                border-radius: 8px;
                                selection-background-color: #dfe9ff;
                                selection-color: #1f2a37;
                                alternate-background-color: #f5f8ff;
                            }

                           QPushButton{
                                background-color: #4a7af0;
                                color: #ffffff;
                                border: none;
                                border-radius: 7px;
                                padding: 9px 16px;
                                font-size: 14px;
                                font-weight: 600;
                            }

                           QPushButton:hover{
                                background-color: #3d6ae0;
                            }

                           QPushButton#clearButton {
                                background-color: #f39c12;
                            }

                           QPushButton#clearButton:hover {
                                background-color: #e68a00;
                            }

                           QPushButton#deleteButton {
                                background-color: #e74c3c;
                            }

                           QPushButton#deleteButton:hover {
                                background-color: #d63b2f;
                            }
                        """)

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Data")) 
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Categoria"))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Montante")) 
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Descrição"))
        self.row2.addWidget(self.description)

        self.add_button.setObjectName("addButton")
        self.clear_button.setObjectName("clearButton")
        self.delete_button.setObjectName("deleteButton")
        self.export_button.setObjectName("exportButton")

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.clear_button)
        self.row3.addWidget(self.delete_button)
        self.row3.addWidget(self.export_button)

        self.filter_row = QHBoxLayout()
        self.filter_row.addWidget(QLabel("Categoria:"))
        self.filter_row.addWidget(self.filter_dropdown)
        self.filter_row.addWidget(QLabel("De:"))
        self.filter_row.addWidget(self.filter_start_date)
        self.filter_row.addWidget(QLabel("Até:"))
        self.filter_row.addWidget(self.filter_end_date)
        self.filter_row.addWidget(self.apply_filter_button)
        self.filter_row.addWidget(self.clear_filter_button)

        self.master_layout.addLayout(self.row1) 
        self.master_layout.addLayout(self.row2) 
        self.master_layout.addLayout(self.row3)
        self.master_layout.addLayout(self.filter_row)
        self.master_layout.addWidget(self.total_label)
        self.master_layout.addWidget(self.monthly_summary_label)

        self.master_layout.addWidget(self.table)
        
        
        self.setLayout(self.master_layout)

        self.load_table()


    def reset_filters(self):
        self.filter_dropdown.setCurrentIndex(0)
        self.filter_start_date.setDate(QDate(2000, 1, 1))
        self.filter_end_date.setDate(QDate.currentDate())
        self.load_table()

    def load_table(self, _index=None):
        self.table.setRowCount(0)

        selected_filter = self.filter_dropdown.currentText()
        start_date = self.filter_start_date.date().toString("yyyy-MM-dd")
        end_date = self.filter_end_date.date().toString("yyyy-MM-dd")

        query = QSqlQuery()
        if selected_filter == "Todas":
            query.prepare("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC")
            query.addBindValue(start_date)
            query.addBindValue(end_date)
        else:
            query.prepare("SELECT * FROM expenses WHERE category = ? AND date BETWEEN ? AND ? ORDER BY date DESC")
            query.addBindValue(selected_filter)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
        query.exec_()

        row = 0
        total = 0.0
        current_month_total = 0.0
        current_month = QDate.currentDate().toString("yyyy-MM")

        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = float(query.value(3))
            description = query.value(4)
            total += amount

            if date.startswith(current_month):
                current_month_total += amount

            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(f"{amount:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

        self.total_label.setText(f"Total: € {total:.2f}")
        self.monthly_summary_label.setText(f"Resumo deste mês: € {current_month_total:.2f}")

    def export_csv(self):
        SAVED_DIR.mkdir(parents=True, exist_ok=True)
        output_path = SAVED_DIR / "expenses_export.csv"
        selected_filter = self.filter_dropdown.currentText()
        start_date = self.filter_start_date.date().toString("yyyy-MM-dd")
        end_date = self.filter_end_date.date().toString("yyyy-MM-dd")

        if selected_filter == "Todas":
            query = QSqlQuery()
            query.prepare("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC")
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            query.exec_()
        else:
            query = QSqlQuery()
            query.prepare("SELECT * FROM expenses WHERE category = ? AND date BETWEEN ? AND ? ORDER BY date DESC")
            query.addBindValue(selected_filter)
            query.addBindValue(start_date)
            query.addBindValue(end_date)
            query.exec_()

        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Id", "Data", "Categoria", "Montante", "Descrição"])
            while query.next():
                writer.writerow([
                    query.value(0),
                    query.value(1),
                    query.value(2),
                    query.value(3),
                    query.value(4),
                ])

        QMessageBox.information(self, "Exportado", f"Arquivo salvo em: {output_path}")

    def clear_fields(self):
        self.amount.clear()
        self.description.clear()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount_text = self.amount.text().strip()
        description = self.description.text().strip()

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Montante inválido", "Introduza um valor numérico válido para a despesa.")
            self.amount.setFocus()
            return

        if amount <= 0:
            QMessageBox.warning(self, "Montante inválido", "O montante deve ser superior a zero.")
            self.amount.setFocus()
            return

        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expenses (date, category, amount, description)
                      VALUES (?, ?, ?, ?)
                        """)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)

        if not query.exec_():
            QMessageBox.critical(self, "Erro", "Não foi possível guardar a despesa.")
            return

        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Nenhuma despesa selecionada", "Escolha uma despesa para eliminar.")
            return

        item = self.table.item(selected_row, 0)
        if item is None:
            QMessageBox.warning(self, "Erro", "Não foi possível identificar a despesa selecionada.")
            return

        expense_id = int(item.text())
        confirm = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente eliminar esta despesa?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = ?")
        query.addBindValue(expense_id)

        if not query.exec_():
            QMessageBox.critical(self, "Erro", "Não foi possível eliminar a despesa.")
            return

        self.load_table()


# Create Database

database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName(str(BASE_DIR / "expense.db"))
if not database.open():
    QMessageBox.critical(None, "Erro", "Não foi possível abrir o banco de dados.")
    sys.exit(1)

query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL,
                description TEXT
            )
            """)


# Run the app
if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()
