from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'db8804322a8d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # groups テーブルの作成
    op.create_table('groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # skill_matrix テーブルの作成
    op.create_table('skill_matrix',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('is_parent', sa.Boolean(), nullable=False),  # Boolean 型に変更
        sa.ForeignKeyConstraint(['group_id'], ['groups.id']),
        sa.ForeignKeyConstraint(['parent_id'], ['skill_matrix.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    # テーブルの削除
    op.drop_table('skill_matrix')
    op.drop_table('groups')
