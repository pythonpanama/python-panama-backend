import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_PROJECT,
    TEST_PROJECT_2,
    TEST_PROJECT_400,
)


# noinspection PyArgumentList
class TestProjectResource(BaseTest):
    """Test all endpoints for the project resource"""

    def test_get_project_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                project_id = self.project.save_to_db().id

                results = c.get(
                    f"/projects/{project_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["project"]["start_date"], "2021-03-16")
                self.assertEqual(data["project"]["end_date"], "2021-04-15")
                self.assertEqual(
                    data["project"]["title"], "REST API para sitio web"
                )
                self.assertEqual(
                    data["project"]["description"],
                    "Un API en Python/Flask para conectar el frontend a "
                    "la base de datos",
                )
                self.assertEqual(
                    data["project"]["goals"],
                    "Generar páginas de forma dinámica para miembros, "
                    "reuniones y proyectos",
                )
                self.assertEqual(data["project"]["status"], "in progress")
                self.assertEqual(data["project"]["admin_id"], 1)

    def test_get_project_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/projects/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Project with id '99' was not found.",
                )

    def test_post_project_201(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()

                results = c.post(
                    "/projects",
                    data=json.dumps(TEST_PROJECT),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Project created successfully."
                )
                self.assertEqual(data["project"]["start_date"], "2021-03-16")
                self.assertEqual(data["project"]["end_date"], "2021-04-15")
                self.assertEqual(
                    data["project"]["title"], "REST API para sitio web"
                )
                self.assertEqual(
                    data["project"]["description"],
                    "Un API en Python/Flask para conectar el frontend a "
                    "la base de datos",
                )
                self.assertEqual(
                    data["project"]["goals"],
                    "Generar páginas de forma dinámica para miembros, "
                    "reuniones y proyectos",
                )
                self.assertEqual(data["project"]["status"], "in progress")
                self.assertEqual(data["project"]["admin_id"], 1)

    def test_post_project_400(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/projects",
                    data=json.dumps(TEST_PROJECT_400),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertTrue("start_date" in data["error"])
                self.assertTrue("title" in data["error"])
                self.assertTrue("description" in data["error"])
                self.assertTrue("goals" in data["error"])
                self.assertTrue("status" in data["error"])

                results = c.post(
                    "/projects",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_post_project_409(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                self.project.save_to_db()

                results = c.post(
                    "/projects",
                    data=json.dumps(TEST_PROJECT),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Project with title "
                    "'REST API para sitio web' already exists.",
                )

    def test_put_project_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                project_id = self.project.save_to_db().id

                results = c.put(
                    f"/projects/{project_id}",
                    data=json.dumps(TEST_PROJECT_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Project modified successfully."
                )
                self.assertEqual(data["project"]["start_date"], "2021-04-16")
                self.assertEqual(data["project"]["end_date"], "2021-05-15")
                self.assertEqual(
                    data["project"]["title"], "Frontend para Python Panamá"
                )
                self.assertEqual(
                    data["project"]["description"],
                    "Sitio web de Python Panamá",
                )
                self.assertEqual(
                    data["project"]["goals"],
                    "Sitio para compartir información relevante",
                )
                self.assertEqual(data["project"]["status"], "completed")
                self.assertEqual(data["project"]["admin_id"], 1)

    def test_put_project_400(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                project_id = self.project.save_to_db().id

                results = c.put(
                    f"/projects/{project_id}",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_project_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/projects/99",
                    data=json.dumps(TEST_PROJECT_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Project with id '99' was not found.",
                )

    def test_put_project_409(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                self.project.save_to_db()
                project_id = self.project_2.save_to_db().id

                results = c.put(
                    f"/projects/{project_id}",
                    data=json.dumps(TEST_PROJECT),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Project with title "
                    "'REST API para sitio web' already exists.",
                )

    def test_delete_project_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                project_id = self.project.save_to_db().id

                results = c.delete(
                    f"/projects/{project_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["project"]["start_date"], "2021-03-16")

    def test_delete_project_404(self):
        with self.client as c:
            with self.app_context:
                results = c.delete(
                    f"/projects/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Project with id '99' was not found.",
                )

    def test_get_projects_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                project_1_id = self.project.save_to_db().id
                project_2_id = self.project_2.save_to_db().id

                results = c.get(
                    f"/projects",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["projects"]), 2)
                self.assertEqual(data["projects"][0]["id"], project_1_id)
                self.assertEqual(data["projects"][1]["id"], project_2_id)

    def test_get_projects_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/projects",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: No projects found.",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
