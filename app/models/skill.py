# app/models/skill.py # noqa: E402
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()

# noqa: E402

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # ここでnameカラムを定義
    description = Column(String)
