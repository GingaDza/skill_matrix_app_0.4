# app/models/database.py

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()




class SkillMatrix(Base):
    __tablename__ = 'skill_matrix'
    
    id = Column(Integer, primary_key=True)
    skill_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    is_parent = Column(Boolean, default=False)  # is_parent Column
    group = relationship("Group", back_populates="skills")


class Group(Base):
    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    skills = relationship("SkillMatrix", back_populates="group")

# データベースの接続文字列を設定
DATABASE_URL = "sqlite:///./your_database.db"  # または sqlite:////Users/sanadatakeshi/Projects/skill_matrix_app_0.4/your_database.db

# SQLAlchemyのエンジンを作成
engine = create_engine(DATABASE_URL)