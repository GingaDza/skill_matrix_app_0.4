# app/models/user.py
from sqlalchemy import Column, Integer, String

from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)  # email カラムを追加

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
