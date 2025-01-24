# app/models/skill_matrix_model.py # noqa: E402

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from app.models.base import Base  # noqa: E402
from typing import List
from app.models.database import Group, SkillMatrix  # noqa: E402

class SkillMatrixModel():
    def __init__(self, db_url="sqlite:///./your_database.db"):
        self.engine = create_engine(db_url)
        Base.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # ヘルパーメソッド: グループの取得
    def _get_group(self, group_name: str):
        return self.session.query(Group).filter(Group.name == group_name).first()

    # ヘルパーメソッド: 親スキルの取得
    def _get_parent(self, group_id: int, parent_name: str):
        return self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == parent_name, SkillMatrix.group_id == group_id, SkillMatrix.is_parent == True).first()

    # ヘルパーメソッド: 子スキルの取得
    def _get_child(self, group_id: int, parent_id: int, child_name: str):
        return self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == child_name, SkillMatrix.group_id == group_id, SkillMatrix.parent_id == parent_id).first()

    def get_skill_matrix(self) -> List[SkillMatrix]:
        """skill_matrixテーブルのレコードをすべて取得する。"""
        return self.session.query(SkillMatrix).all()

    def add_skill(self, group_name: str, parent_name: str, child_name: str, level: int) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = None
            if parent_name:
                parent = self._get_parent(group.id, parent_name)
                if not parent:
                    return False

            # 親スキルと子スキルの処理
            if parent and child_name:
                existing_child = self._get_child(group.id, parent.id, child_name)
                if existing_child:
                    return False
                new_skill = SkillMatrix(skill_name=str(level), group_id=group.id, parent_id=parent.id, is_parent=False)
            else:
                new_skill = SkillMatrix(skill_name=str(level), group_id=group.id, is_parent=False)

            self.session.add(new_skill)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding skill: {e}")
            self.session.rollback()
            return False

    def rename_skill(self, group_name: str, parent_name: str, child_name: str, skill_level: int, new_skill_level:int) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = None
            if parent_name:
                parent = self._get_parent(group.id, parent_name)
                if not parent:
                    return False

            skill = None
            if parent and child_name:
                skill = self._get_child(group.id, parent.id, str(skill_level))
            elif parent:
                skill = self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == str(skill_level), SkillMatrix.group_id == group.id, SkillMatrix.parent_id == parent.id).first()
            else:
                skill = self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == str(skill_level), SkillMatrix.group_id == group.id).first()

            if not skill:
                return False

            skill.skill_name = str(new_skill_level)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error renaming skill: {e}")
            self.session.rollback()
            return False

    def delete_skill(self, group_name: str, parent_name: str, child_name: str, skill_level: int) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = None
            skill = None
            if parent_name and child_name:
                parent = self._get_parent(group.id, parent_name)
                if not parent:
                    return False
                skill = self._get_child(group.id, parent.id, str(skill_level))
            elif parent_name:
                parent = self._get_parent(group.id, parent_name)
                if not parent:
                    return False
                skill = self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == str(skill_level), SkillMatrix.group_id == group.id, SkillMatrix.parent_id == parent.id).first()
            else:
                skill = self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == str(skill_level), SkillMatrix.group_id == group.id).first()

            if not skill:
                return False

            self.session.delete(skill)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting skill: {e}")
            self.session.rollback()
            return False

    def add_group(self, group_name: str) -> bool:
        try:
            existing_group = self._get_group(group_name)
            if existing_group:
                return False

            new_group = Group(name=group_name)
            self.session.add(new_group)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding group: {e}")
            self.session.rollback()
            return False

    def rename_group(self, old_group_name: str, new_group_name: str) -> bool:
        try:
            existing_group = self._get_group(new_group_name)
            if existing_group:
                return False

            group = self._get_group(old_group_name)
            if not group:
                return False

            group.name = new_group_name
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error renaming group: {e}")
            self.session.rollback()
            return False

    def delete_group(self, group_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            self.session.delete(group)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting group: {e}")
            self.session.rollback()
            return False

    def add_participant(self, group_name: str, participant_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            new_participant = SkillMatrix(skill_name=participant_name, group_id=group.id)
            self.session.add(new_participant)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding participant: {e}")
            self.session.rollback()
            return False

    def rename_participant(self, group_name: str, old_participant_name: str, new_participant_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False
            participant = self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == old_participant_name, SkillMatrix.group_id == group.id).first()
            if not participant:
                return False
            participant.skill_name = new_participant_name
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error renaming participant: {e}")
            self.session.rollback()
            return False

    def delete_participant(self, group_name: str, participant_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False
            participant = self.session.query(SkillMatrix).filter(SkillMatrix.skill_name == participant_name, SkillMatrix.group_id == group.id).first()
            if not participant:
                return False
            self.session.delete(participant)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting participant: {e}")
            self.session.rollback()
            return False

    def add_parent_skill(self, group_name: str, parent_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            existing_parent = self._get_parent(group.id, parent_name)
            if existing_parent:
                return False

            new_parent = SkillMatrix(skill_name=parent_name, group_id=group.id, is_parent=True)
            self.session.add(new_parent)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding parent skill: {e}")
            self.session.rollback()
            return False

    def rename_parent_skill(self, group_name: str, old_parent_name: str, new_parent_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = self._get_parent(group.id, old_parent_name)
            if not parent:
                return False

            parent.skill_name = new_parent_name
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error renaming parent skill: {e}")
            self.session.rollback()
            return False

    def delete_parent_skill(self, group_name: str, parent_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = self._get_parent(group.id, parent_name)
            if not parent:
                return False

            self.session.delete(parent)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting parent skill: {e}")
            self.session.rollback()
            return False

    def add_child_skill(self, group_name: str, parent_name: str, child_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = self._get_parent(group.id, parent_name)
            if not parent:
                return False

            existing_child = self._get_child(group.id, parent.id, child_name)
            if existing_child:
                return False

            new_child = SkillMatrix(skill_name=child_name, group_id=group.id, parent_id=parent.id, is_parent=False)
            self.session.add(new_child)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error adding child skill: {e}")
            self.session.rollback()
            return False

    def rename_child_skill(self, group_name: str, parent_name: str, old_child_name: str, new_child_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = self._get_parent(group.id, parent_name)
            if not parent:
                return False

            child = self._get_child(group.id, parent.id, old_child_name)
            if not child:
                return False

            child.skill_name = new_child_name
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error renaming child skill: {e}")
            self.session.rollback()
            return False

    def delete_child_skill(self, group_name: str, parent_name: str, child_name: str) -> bool:
        try:
            group = self._get_group(group_name)
            if not group:
                return False

            parent = self._get_parent(group.id, parent_name)
            if not parent:
                return False

            child = self._get_child(group.id, parent.id, child_name)
            if not child:
                return False

            self.session.delete(child)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting child skill: {e}")
            self.session.rollback()
            return False
