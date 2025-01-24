# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

# データベースの接続文字列を設定
DATABASE_URL = "sqlite:///./your_database.db"  # または sqlite:////Users/sanadatakeshi/Projects/skill_matrix_app_0.4/your_database.db

# SQLAlchemyのエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションを作成するためのセッションメーカーを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# モデルを読み込み、テーブルを作成
def create_database():
    Base.metadata.create_all(bind=engine)