from PyQt5.QtWidgets import QLineEdit, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Data")
        self.setGeometry(100, 100, 600, 400)

        # レイアウト設定
        self.layout = QVBoxLayout()

        # 入力フィールド
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter employee name")
        self.layout.addWidget(self.name_input)

        self.department_input = QLineEdit(self)
        self.department_input.setPlaceholderText("Enter department")
        self.layout.addWidget(self.department_input)

        # 追加ボタン
        self.add_button = QPushButton("Add Employee")
        self.add_button.clicked.connect(self.add_employee)
        self.layout.addWidget(self.add_button)

        # テーブル設定
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # テーブルの列数設定
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Department"])

        # データの取得とテーブルへの表示
        self.load_data()

        # 中央ウィジェット設定
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        # データの取得
        employees = get_all_employees()

        # テーブルの行数設定
        self.table.setRowCount(len(employees))

        # テーブルにデータを設定
        for row, employee in enumerate(employees):
            self.table.setItem(row, 0, QTableWidgetItem(str(employee.id)))
            self.table.setItem(row, 1, QTableWidgetItem(employee.name))
            self.table.setItem(row, 2, QTableWidgetItem(employee.department))

    def add_employee(self):
        name = self.name_input.text()
        department = self.department_input.text()

        # 新しい従業員をデータベースに追加
        new_employee = Employee(name=name, department=department)
        session.add(new_employee)
        session.commit()

        # データの再読み込み
        self.load_data()

        # 入力フィールドをクリア
        self.name_input.clear()
        self.department_input.clear()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
