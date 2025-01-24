# app/models/group.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # SkillMatrix との関連付け
    skill_matrices = relationship('SkillMatrix', back_populates='group', lazy='select')