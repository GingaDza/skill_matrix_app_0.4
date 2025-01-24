# tests/test_get_skill_matrix.py

import unittest
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

class TestSkillMatrixModel(unittest.TestCase):

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

    def test_get_skill_matrix(self):
        # サンプルグループを作成
        group = self.Group(name="Test Group")
        self.session.add(group)
        self.session.commit()
        # サンプルスキルを作成
        new_skill = self.SkillMatrix(skill_name="Test Skill", group_id=group.id, is_parent=True)
        self.session.add(new_skill)
        self.session.commit()

        result = self.session.query(self.SkillMatrix).all()
        self.assertGreater(len(result), 0)

    def test_create_skill_matrix(self):
        # skill_matrix を作成するテスト
        group = self.Group(name="Test Group")
        self.session.add(group)
        self.session.commit()

        new_skill = self.SkillMatrix(skill_name="New Skill", group_id=group.id, is_parent=True)
        self.session.add(new_skill)
        self.session.commit()

        # 作成したデータが保存されているか確認
        saved_skill = self.session.query(self.SkillMatrix).filter_by(skill_name="New Skill").first()
        self.assertIsNotNone(saved_skill)

    def tearDown(self):
        # セッションを閉じる
        self.session.close()

if __name__ == "__main__":
    unittest.main()