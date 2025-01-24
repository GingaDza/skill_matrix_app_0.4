# tests/test_models.py

import pytest # noqa: E402
from sqlalchemy import create_engine # noqa: E402
from sqlalchemy.orm import sessionmaker # noqa: E402
from app.models.skill_matrix_model import SkillMatrix, Group # noqa: E402
from app.models.base import Base  # Baseクラスをインポート # noqa: E402

@pytest.fixture
def setup_database():
    # メモリ上のSQLiteデータベースを作成
    engine = create_engine("sqlite:///:memory:")  # メモリ上のSQLiteデータベース
    Base.metadata.create_all(engine)  # テーブルを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # テスト関数にセッションを渡す

    # テスト後にセッションを閉じる
    session.close()
    engine.dispose()

def test_create_group_and_skill(setup_database):
    session = setup_database # noqa: E402

    # Groupの作成
    group = Group(name="Development")
    session.add(group)
    session.commit()  # セッションをコミットしてデータを保存

    # SkillMatrixの作成
    skill = SkillMatrix(skill_name="Python", group_id=group.id)
    session.add(skill)
    session.commit()  # セッションをコミットしてデータを保存

    # テストデータの検証
    saved_group = session.query(Group).filter_by(name="Development").first()
    saved_skill = session.query(SkillMatrix).filter_by(skill_name="Python").first()

    # 検証: グループとスキルが正しく保存されているか
    assert saved_group is not None
    assert saved_skill is not None
    assert saved_skill.group_id == saved_group.id
