import unittest

from models.project import ProjectModel
from tests.base_test import BaseTest


class TestProject(BaseTest):
    """Test all methods for the ProjectModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.project.start_date, "2021-03-16")
            self.assertEqual(self.project.end_date, "2021-04-15")
            self.assertEqual(self.project.title, "REST API para sitio web")
            self.assertEqual(
                self.project.description,
                "Un API en Python/Flask para conectar el frontend a la base "
                "de datos",
            )
            self.assertEqual(
                self.project.goals,
                "Generar páginas de forma dinámica para miembros, reuniones "
                "y proyectos",
            )
            self.assertEqual(self.project.status, "in progress")
            self.assertEqual(self.project.admin_id, 1)

    def test_find_all(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            poject_id = self.project.save_to_db().id

            projects = ProjectModel.find_all()

            self.assertEqual(projects[0].id, poject_id)

    def test_find_by_admin_id(self):
        with self.app_context:
            self.role.save_to_db()
            admin_id = self.member.save_to_db().id
            poject_id = self.project.save_to_db().id

            projects = ProjectModel.find_by_admin_id(admin_id)

            self.assertEqual(projects[0].id, poject_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            poject_id = self.project.save_to_db().id

            project = ProjectModel.find_by_id(poject_id)

            self.assertEqual(project.title, "REST API para sitio web")

    def test_find_by_status(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            poject_id = self.project.save_to_db().id

            projects = ProjectModel.find_by_status("in progress")

            self.assertEqual(projects[0].id, poject_id)


if __name__ == "__main__":
    unittest.main()
