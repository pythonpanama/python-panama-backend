import unittest

from models.member import MemberModel
from models.project import ProjectModel
from tests.base_test import BaseTest


class TestProject(BaseTest):
    """Test all methods for the ProjectModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.project_1.start_date, "2021-03-16")
            self.assertEqual(self.project_1.end_date, "2021-04-15")
            self.assertEqual(self.project_1.title, "REST API para sitio web")
            self.assertEqual(
                self.project_1.description,
                "Un API en Python/Flask para conectar el frontend a la base "
                "de datos",
            )
            self.assertEqual(
                self.project_1.goals,
                "Generar páginas de forma dinámica para miembros, reuniones "
                "y proyectos",
            )
            self.assertEqual(self.project_1.status, "in progress")
            self.assertEqual(self.project_1.admin_id, 1)

    def test_find_all(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            poject_id = self.project_1.save_to_db().id

            projects = ProjectModel.find_all()

            self.assertEqual(projects[0].id, poject_id)

    def test_find_by_admin_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            admin_id = self.member_1.save_to_db().id
            poject_id = self.project_1.save_to_db().id

            projects = ProjectModel.find_by_admin_id(admin_id)

            self.assertEqual(projects[0].id, poject_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            poject_id = self.project_1.save_to_db().id

            project = ProjectModel.find_by_id(poject_id)

            self.assertEqual(project.title, "REST API para sitio web")

    def test_find_by_status(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            poject_id = self.project_1.save_to_db().id

            projects = ProjectModel.find_by_status("in progress")

            self.assertEqual(projects[0].id, poject_id)

    def test_projects_members_relation(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            project_id = self.project_1.save_to_db().id
            member_id = self.member_1.save_to_db().id

            project = ProjectModel.find_by_id(project_id)
            member = MemberModel.find_by_id(member_id)
            project.members.append(member)

            self.assertEqual(project.members[0].email, "jperez@ppty.com")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
