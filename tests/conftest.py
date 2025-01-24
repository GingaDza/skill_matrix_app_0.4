import pytest
from unittest.mock import MagicMock

@pytest.fixture
def skill_matrix_model_mock():
    # モックを作成
    mock = MagicMock()
    # 必要に応じてモックの動作をカスタマイズ
    mock.fetch_skill_levels.return_value = ["Skill 1", "Skill 2"]
    return mock
