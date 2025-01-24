from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QHBoxLayout, QScrollArea
from app.models.skill_matrix_model import SkillMatrix  # 修正したインポート

class CustomTab(QWidget):
    def __init__(self, parent=None, group_name=None):
        super().__init__(parent)
        self.group_name = group_name
        self.skill_matrix_model = SkillMatrix()  # 修正したインスタンス化
        self.setLayout(QVBoxLayout())
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(QVBoxLayout())
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.skill_level_combos = {}

        self.setup_ui()

    def setup_ui(self):
        if self.group_name:
            skill_matrix = self.skill_matrix_model.get_skill_matrix()

            # スキルレベルを取得し、コンボボックスに設定
            skill_levels = [str(i) for i in range(1, 11)]  # 例：1から10までのスキルレベル

            # 親カテゴリーと子カテゴリーを抽出
            parent_categories = []
            child_categories = {}
            for item in skill_matrix:
                if item.group.name == self.group_name and item.is_parent == True:
                    parent_categories.append(item.skill_name)
                elif item.group.name == self.group_name and item.parent_id is not None and item.is_parent == False:
                    if item.parent.skill_name not in child_categories:
                        child_categories[item.parent.skill_name] = []
                    child_categories[item.parent.skill_name].append(item.skill_name)

            for parent in parent_categories:
                if parent in child_categories:
                    for child in child_categories[parent]:
                        hbox = QHBoxLayout()
                        label = QLabel(child)
                        hbox.addWidget(label)
                        combo = QComboBox()
                        combo.addItems(skill_levels)
                        self.skill_level_combos[(parent, child)] = combo
                        hbox.addWidget(combo)
                        self.scroll_area_widget.layout().addLayout(hbox)
                else:
                    hbox = QHBoxLayout()
                    label = QLabel(parent)
                    hbox.addWidget(label)
                    combo = QComboBox()
                    combo.addItems(skill_levels)
                    self.skill_level_combos[(parent, None)] = combo
                    hbox.addWidget(combo)
                    self.scroll_area_widget.layout().addLayout(hbox)

            self.saveButton = QPushButton("保存")
            self.scroll_area_widget.layout().addWidget(self.saveButton)
            self.saveButton.clicked.connect(self.save_settings)


    def save_settings(self):
        # 保存処理をここに実装
        print("設定を保存します")
        for (parent, child), combo in self.skill_level_combos.items():
            level = combo.currentText()
            print(f"parent: {parent}, child: {child}, level: {level}")
