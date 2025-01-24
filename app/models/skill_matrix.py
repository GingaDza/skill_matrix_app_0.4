# app/models/skill_matrix.py # noqa: E402

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.group import Group  # Group クラスのインポート

class SkillMatrix(Base):
    __tablename__ = 'skill_matrix'

    id = Column(Integer, primary_key=True)  # noqa: E741
    skill_name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))  # Groupとの外部キー
    parent_id = Column(Integer, ForeignKey('skill_matrix.id'))
    is_parent = Column(Boolean, default=False)

    # groupリレーションの定義
    group = relationship(Group, back_populates='skill_matrices', lazy='select')

    # 自己参照リレーションの定義 (親子関係)
    parent = relationship('SkillMatrix', remote_side=[id], backref="children", foreign_keys=[parent_id], lazy='select')

    def __init__(self, skill_name=None, group_id=None, is_parent=False):
        self.skill_name = skill_name
        self.group_id = group_id
        self.is_parent = is_parent  # noqa: E701
