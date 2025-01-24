# app/initialize_db.py # noqa: E402
from app.models.database import engine, DATABASE_URL
from app.models.base import Base # noqa: E402
from sqlalchemy import inspect
from app.models.database import Group, SkillMatrix
from sqlalchemy.orm import sessionmaker

def init_db():
    # 既存のテーブルを削除
    inspector = inspect(engine)
    for table_name in reversed(inspector.get_table_names()):
        if table_name != 'alembic_version':  # alembicのテーブル以外を削除
            Base.metadata.drop_all(bind=engine, tables=[Base.metadata.tables[table_name]])

    # データベースの初期化（テーブル作成など） # noqa: E402
    Base.metadata.create_all(bind=engine)

    # 初期データの投入
    session = sessionmaker(bind=engine)()
    try:
        # グループの追加
        group_a = Group(name="Test Group")
        session.add(group_a)
        session.commit()  # 変更をデータベースに保存

        # スキルの追加（親カテゴリとして）
        skill_test = SkillMatrix(skill_name="Test Skill", group_id=group_a.id, is_parent=True)
        session.add(skill_test)
        
        # 参加者の追加（子カテゴリとして）
        skill1 = SkillMatrix(skill_name="1", group_id=group_a.id, is_parent=False)
        skill1.parent = skill_test  # 親を設定
        session.add(skill1)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error init_db {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
