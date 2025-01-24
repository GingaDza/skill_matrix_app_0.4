import unittest
from unittest.mock import MagicMock
from app.models.skill_matrix_model import SkillMatrix


# モッククラスの定義
class MockSkillMatrixModel:
    def get_skill_matrix(self):
        # テスト用のダミーデータを返す
        return [
            MockSkillItem(group_name="Group1", parent_name="ParentA", child_name="Child1", skill_name="Skill1"),
            MockSkillItem(group_name="Group1", parent_name="ParentA", child_name="Child2", skill_name="Skill2"),
            MockSkillItem(group_name="Group1", parent_name="ParentB", child_name=None, skill_name="Skill3"),
            MockSkillItem(group_name="Group1", parent_name=None, child_name=None, skill_name="Skill4"),
            MockSkillItem(group_name="Group2", parent_name=None, child_name=None, skill_name="Skill5"),
            MockSkillItem(group_name="Group2", parent_name="ParentC", child_name="ChildX", skill_name="Skill6"),
        ]

class MockSkillItem:
    def __init__(self, group_name, parent_name=None, child_name=None, skill_name="Skill", is_parent=False):
        self.group = MockGroup(group_name)
        self.parent = MockSkill(parent_name) if parent_name else None
        self.skill_name = child_name if child_name else skill_name
        self.is_parent = is_parent
        self.children = []  # children 属性を追加

    def __repr__(self):
        return f"SkillItem(group={self.group.name}, parent={self.parent.skill_name if self.parent else None}, child={self.skill_name}, is_parent={self.is_parent})"

class MockGroup:
    def __init__(self, name):
        self.name = name

class MockSkill:
    def __init__(self, name):
        self.skill_name = name

class MockCurrentItem:
    def __init__(self, text):
        self.text_value = text
    
    def text(self):
         return self.text_value

class MockCategorySettings:
    def __init__(self):
        self.parent_category_list = MockListWidget()
        self.child_category_list = MockListWidget()

class MockListWidget:
    def __init__(self):
        self.current_item = None
        self.items = []

    def currentItem(self):
        return self.current_item
    
    def setCurrentItem(self, item):
        self.current_item = item

    def setCurrentRow(self, index):
      if 0 <= index < len(self.items):
          self.current_item = MockCurrentItem(self.items[index])
      else:
          self.current_item = None

    def count(self):
        return len(self.items)

    def addItems(self, items):
        self.items.extend(items)

    def clear(self):
        self.items = []

class TestSkillSettings(unittest.TestCase):
    def setUp(self):
        self.controller = MockController()
        self.initial_settings_tab = MockInitialSettingsTab(self.controller)
        self.skill_settings = SkillSettings(self.controller, self.initial_settings_tab)
        self.skill_settings.skill_matrix_model = MockSkillMatrixModel()
        self.skill_settings.initial_settings_tab = self.initial_settings_tab  # SkillSettings に InitialSettingsTab を設定
        self.skill_settings.initial_settings_tab.group_settings = MockGroupSettings()
        self.skill_settings.initial_settings_tab.category_settings = MockCategorySettings()

    def test_fetch_skill_levels_parent_and_child(self):
        # 親カテゴリと子カテゴリが選択されている場合のテスト
        skill_levels = self.skill_settings._fetch_skill_levels("Group1", "ParentA", "Child1")
        self.assertIn("Skill1", skill_levels)

    def test_fetch_skill_levels_parent_only(self):
        # 親カテゴリのみが選択されている場合のテスト
        skill_levels = self.skill_settings._fetch_skill_levels("Group1", "ParentB", None)
        self.assertIn("Skill3", skill_levels)

    def test_fetch_skill_levels_no_parent_no_child(self):
        # 親カテゴリも子カテゴリも選択されていない場合のテスト
        skill_levels = self.skill_settings._fetch_skill_levels("Group1", None, None)
        self.assertIn("Skill4", skill_levels)

    def test_fetch_skill_levels_no_group(self):
        # グループが選択されていない場合のテスト
        skill_levels = self.skill_settings._fetch_skill_levels(None, "ParentA", "Child1")
        self.assertEqual(skill_levels, [])

class MockController:
    # 仮のコントローラークラス
    pass

class MockInitialSettingsTab:
    def __init__(self, controller):
        self.category_settings = MockCategorySettings()
        self.group_settings = MockGroupSettings()
        self.skill_settings = SkillSettings(controller, self)  # SkillSettings のインスタンスを作成

    def update_skill_group_combo(self):
        pass

class MockGroupSettings:
    def __init__(self):
        self.group_list = MockListWidget()

    def update_skill_group_combo_from_list(self, current, previous):
        pass

    def update_parent_list(self, current, previous):
        pass

if __name__ == '__main__':
    unittest.main()