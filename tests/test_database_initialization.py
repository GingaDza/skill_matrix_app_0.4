# tests/test_database_initialization.py
import pytest  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from app.models import Base, User  # Userモデルを使用する場合 # noqa: E402


DATABASE_URL = "sqlite:///:memory:"  # メモリ内データベースを使用する例

@pytest.fixture
def db_session():
    # エンジン作成
    engine = create_engine(DATABASE_URL, echo=True)
    
    # テーブルを作成
    Base.metadata.create_all(bind=engine)
    
    # セッション作成
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session  # テスト後にセッションをクリーンアップ
    
    # テスト後にセッションを閉じる
    session.close()

def test_db_connection(db_session):
    assert db_session is not None  # セッションが正しく作成されていればテストが通る

def test_create_user(db_session):
    # 新しいユーザーを作成
    new_user = User(name="Test User", email="test@example.com")
    
    # データベースに追加
    db_session.add(new_user)
    db_session.commit()
    
    # データベースからユーザーを取得
    fetched_user = db_session.query(User).filter_by(email="test@example.com").first()
    
    # ユーザーが正しく保存されたことを確認
    assert fetched_user is not None
    assert fetched_user.name == "Test User"
    assert fetched_user.email == "test@example.com"

def test_delete_user(db_session):
    # ユーザーを作成して保存
    new_user = User(name="Test User", email="delete@example.com")
    db_session.add(new_user)
    db_session.commit()
    
    # ユーザーを削除
    db_session.delete(new_user)
    db_session.commit()
    
    # 削除後にユーザーを再度検索
    deleted_user = db_session.query(User).filter_by(email="delete@example.com").first()
    
    # ユーザーが削除されたことを確認
    assert deleted_user is None
