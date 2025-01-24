# app/ui/dialogs.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel, QComboBox

class AddParticipantDialog(QDialog):
    def __init__(self, parent=None, title="参加者を追加", current_group=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        if current_group:
            layout.addWidget(QLabel(f"現在のグループ: {current_group}"))

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("参加者名を入力してください")
        layout.addWidget(self.input_field)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def get_input_text(self):
        return self.input_field.text()

class AddCategoryDialog(QDialog):
    def __init__(self, parent=None, title="Add Category", initial_text=""):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        # 入力フィールド
        self.input_field = QLineEdit(self)
        if initial_text:
            self.input_field.setText(initial_text)
        layout.addWidget(QLabel("Enter category name:"))
        layout.addWidget(self.input_field)

        # ボタン
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.buttons)

        # ボタンシグナル
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_input_text(self):
        return self.input_field.text()

class DeleteConfirmationDialog(QDialog):
    def __init__(self, parent=None, title="Delete Confirmation", message="Are you sure you want to delete this category?"):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        # メッセージ
        layout.addWidget(QLabel(message))

        # ボタン
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.buttons)

        # ボタンシグナル
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)


class EditSkillDialog(QDialog):
    def __init__(self, parent=None, title="Edit Skill", initial_skill_name=""):
        super().__init__(parent)
        self.setWindowTitle(title)

        layout = QVBoxLayout(self)

        # スキル名ラベルと入力フィールド
        layout.addWidget(QLabel("スキルレベル:"))

        # スキルレベルコンボボックス
        self.skill_level_combo = QComboBox(self)
        self.skill_level_combo.addItems([str(i) for i in range(1, 11)]) # 1から10までのコンボボックス
        layout.addWidget(self.skill_level_combo)


        # ボタン
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(self.buttons)

        # ボタンシグナル
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.skill_level = 0
        # 初期値の設定
        if initial_skill_name:
             self.skill_level_combo.setCurrentText(initial_skill_name)

    def get_skill_name(self):
        return self.skill_level_combo.currentText()

    def get_skill_level(self):
         return int(self.skill_level_combo.currentText())