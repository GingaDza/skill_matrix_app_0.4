import unittest
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text

class TestGroupCombo(unittest.TestCase):
    def setUp(self):
         # Create a new declarative base for this test class
        Base = declarative_base()
        class SkillMatrix(Base):
            __tablename__ = "skill_matrix"
            id = Column(Integer, primary_key=True)
            skill_name = Column(String, nullable=False)
            group_id = Column(Integer, ForeignKey("groups.id"))
            is_parent = Column(Boolean, default=False) # Add is_parent Column
            group = relationship("Group", back_populates="skills")

        class Group(Base):
            __tablename__ = "groups"
            id = Column(Integer, primary_key=True)
            name = Column(String, nullable=False)
            skills = relationship("SkillMatrix", back_populates="group")
        
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.SkillMatrix = SkillMatrix
        self.Group = Group
        self.Base = Base

    def test_group_table_exists(self):
      # groupsテーブルが存在するか確認
       with self.engine.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='groups'")
            )
            self.assertIsNotNone(result.fetchone())
    
    def test_skill_matrix_table_exists(self):
         # skill_matrixテーブルが存在するか確認
        with self.engine.connect() as connection:
            result = connection.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='skill_matrix'")
            )
            self.assertIsNotNone(result.fetchone())
    
    def tearDown(self):
      self.session.close()

if __name__ == "__main__":
    unittest.main()