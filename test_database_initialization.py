# test_database_initialization.py
import unittest
import subprocess
import sqlite3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.database import DATABASE_URL  # 修正: app.models.database からインポート
from app.models import Group

class TestDatabaseInitialization(unittest.TestCase):

    def setUp(self):
        # データベースの初期化を行う
        subprocess.call(['python', 'app/initialize_db.py'])

        # データベースに接続してテーブルが存在するか確認
        self.conn = sqlite3.connect(DATABASE_URL.split("sqlite:///")[-1])
        self.cursor = self.conn.cursor()

        # グループデータが存在しない場合、挿入する
        self.cursor.execute("SELECT COUNT(*) FROM groups;")
        count = self.cursor.fetchone()[0]
        if count == 0:
            self.cursor.execute("INSERT INTO groups (name) VALUES ('Group A'), ('Group B'), ('Group C');")
            self.conn.commit()

    def tearDown(self):
        # テスト後にデータベース接続を閉じる
        self.conn.close()

    def test_groups_table_exists(self):
        # groupsテーブルが存在するか確認
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='groups';")
        table = self.cursor.fetchone()
        self.assertIsNotNone(table, "groupsテーブルが存在しません。")

    def test_groups_data_exists(self):
        # groupsテーブルにデータが存在するか確認
        self.cursor.execute("SELECT * FROM groups LIMIT 1;")
        group = self.cursor.fetchone()
        self.assertIsNotNone(group, "グループデータが存在しません。")

if __name__ == "__main__":
    unittest.main()