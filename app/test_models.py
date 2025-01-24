import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.skill_matrix_model import SkillMatrix, Group
from app.models.base import Base  # Baseクラスをインポート

@pytest.fixture
def setup_database():
    engine = create_engine("sqlite:///:memory:")  # メモリ上のSQLiteデータベース
    Base.metadata.create_all(engine)  # テーブルを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session  # テスト関数にセッションを渡す

    session.close()
    engine.dispose()

def test_create_group_and_skill(setup_database):
    session = setup_database

    # Groupの作成
    group = Group(name="Development")
    session.add(group)
    session.commit()

    # SkillMatrixの作成
    skill = SkillMatrix(skill_name="Python", group_id=group.id)
    session.add(skill)
    session.commit()

    # テストデータの検証
    saved_group = session.query(Group).filter_by(name="Development").first()
    saved_skill = session.query(SkillMatrix).filter_by(skill_name="Python").first()

    assert saved_group is not None
    assert saved_skill is not None
    assert saved_skill.group_id == saved_group.id
