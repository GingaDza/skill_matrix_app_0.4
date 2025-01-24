# データベースモデル

## データベースの種類

*   SQLite (ファイルベース) を使用します。
*   データベースファイル名は `skill_matrix.db` です。

## テーブル構成

1.  **users (ユーザーテーブル)**
    *   `id`: INTEGER, PRIMARY KEY
    *   `name`: TEXT (ユーザー名)
    *   `email`: TEXT (ユーザーメールアドレス)

2.  **items (アイテムテーブル)**
    *   `id`: INTEGER, PRIMARY KEY
    *   `name`: TEXT (アイテム名)
    *   `price`: REAL (アイテム価格)

3.  **skills (スキルテーブル)**
    *   `id`: INTEGER, PRIMARY KEY
    *   `name`: TEXT (スキル名)
    *   `level`: INTEGER (スキルレベル)

4.  **tabs (タブテーブル)**
    *   `id`: INTEGER, PRIMARY KEY
    *   `name`: TEXT (タブ名)
    *   `user_id`: INTEGER, FOREIGN KEY referencing `users.id`
    *   `content_type`: TEXT (タブのコンテンツタイプ)
    *   `content_config`: TEXT (タブのコンテンツ設定)

5.  **user_items (ユーザーアイテムテーブル)**
    *   `user_id`: INTEGER, FOREIGN KEY referencing `users.id`, PRIMARY KEY
    *   `item_id`: INTEGER, FOREIGN KEY referencing `items.id`, PRIMARY KEY

6.  **user_skills (ユーザー スキルテーブル)**
    *   `user_id`: INTEGER, FOREIGN KEY referencing `users.id`, PRIMARY KEY
    *   `skill_id`: INTEGER, FOREIGN KEY referencing `skills.id`, PRIMARY KEY

## リレーションシップ

*   **users (1:N) user_items**: 一人のユーザーは複数のアイテムを持つ。
*   **items (1:N) user_items**: 一つのアイテムは複数のユーザーによって所有される。
*   **users (1:N) user_skills**: 一人のユーザーは複数のスキルを持つ。
*   **skills (1:N) user_skills**: 一つのスキルは複数のユーザーによって習得される。
*   **users (1:N) tabs**: 一人のユーザーは複数のタブを持つ。

## ORM

*   SQLAlchemy ORM を使用してデータベースを操作します。
*   各テーブルに対応するモデルクラスは `app/models/skill_model.py` に定義されています。

# データベースモデル

## データベースの種類

* SQLite (ファイルベース) を使用します。
* データベースファイル名は `test.db` です。


## テーブル構成

現在、`skills` テーブルのみ定義されています。

1. **skills (スキルテーブル)**
    * `id`: INTEGER, PRIMARY KEY
    * `name`: TEXT (スキル名)
    * `description`: TEXT (スキル説明)


## 今後の拡張性