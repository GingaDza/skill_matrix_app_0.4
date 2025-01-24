# app/models/group_model.py # noqa: E402
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # skill_matrix との関係を定義
    skills = relationship("SkillMatrix", back_populates="group")
