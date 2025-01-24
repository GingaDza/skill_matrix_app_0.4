import os
import sys
import logging
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from database import Base, engine


# プロジェクトルートを Python パスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

# ログ設定
logging.basicConfig(level=logging.INFO)
logging.info(f"Python Path in alembic/env.py: {sys.path}")

# 必要なモジュールをインポート
try:
    from app.models.database import Base, engine
except ModuleNotFoundError as e:
    logging.error(f"Failed to import app.models.database: {e}")
    raise

# Alembic の Config オブジェクト（.ini ファイルの値にアクセス可能）
config = context.config

# ログ設定を読み込む
if config.config_file_name:
    fileConfig(config.config_file_name)

# マイグレーション対象のメタデータを設定
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """オフラインモードでマイグレーションを実行"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """オンラインモードでマイグレーションを実行"""
    try:
        connectable = engine
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        logging.error(f"Failed to run migrations: {e}")
        raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
