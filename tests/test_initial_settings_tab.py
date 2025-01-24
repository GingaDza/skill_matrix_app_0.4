# tests/test_initial_settings_tab.py

import pytest # noqa: E402
from unittest.mock import MagicMock # noqa: E402
from app.ui.initial_settings_tab import InitialSettingsTab # noqa: E402
from pytestqt import qtbot # noqa: E402

def test_initial_settings_tab_import():
    # InitialSettingsTab クラスが正しくインポートされているか
    assert InitialSettingsTab is not None, "InitialSettingsTab is not imported properly"

def test_fetch_skill_levels_method(qtbot):
    # controllerをモックする
    mock_controller = MagicMock()

    # InitialSettingsTabのインスタンスを作成
    initial_settings_tab = InitialSettingsTab(mock_controller)

    # イベントループを進める
    qtbot.addWidget(initial_settings_tab)

    # fetch_skill_levels メソッドが存在し、呼び出せることを確認
    assert hasattr(initial_settings_tab, 'fetch_skill_levels'), "fetch_skill_levels method is missing"
    
    # 実際に呼び出して戻り値が返されるか確認（モックで簡易的に呼び出す）
    result = initial_settings_tab.fetch_skill_levels(None, None, "")
    assert result is not None, "fetch_skill_levels returned None"
