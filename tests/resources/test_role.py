import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_ROLE,
    TEST_ROLE_2,
    TEST_ROLE_400,
)


# noinspection PyArgumentList
class TestRoleResource(BaseTest):
    """Test all endpoints for the role resource"""

    def test_get_role_200(self):
        with self.client as c:
            with self.app_context:
                role_id = self.role.save_to_db().id

                results = c.get(
                    f"/roles/{role_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "admin")

    def test_get_role_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/roles/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Role with id '99' was not found.",
                )

    def test_post_role_201(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "admin")

    def test_post_role_400(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE_400),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertTrue("role_name" in data["error"])

    def test_post_role_409(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()

                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Role with role_name "
                    "'admin' already exists.",
                )

    def test_put_role_200(self):
        with self.client as c:
            with self.app_context:
                role_id = self.role.save_to_db().id

                results = c.put(
                    f"/roles/{role_id}",
                    data=json.dumps(TEST_ROLE_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "member")

    def test_put_role_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/roles/99",
                    data=json.dumps(TEST_ROLE_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Role with id '99' was not found.",
                )

    def test_put_role_409(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                role_id = self.role_2.save_to_db().id

                results = c.put(
                    f"/roles/{role_id}",
                    data=json.dumps(TEST_ROLE),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Role with role_name "
                    "'admin' already exists.",
                )

    def test_delete_role_200(self):
        with self.client as c:
            with self.app_context:
                role_id = self.role.save_to_db().id

                results = c.delete(
                    f"/roles/{role_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "admin")

    def test_delete_role_404(self):
        with self.client as c:
            with self.app_context:
                results = c.delete(
                    f"/roles/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Role with id '99' was not found.",
                )

    def test_get_roles_200(self):
        with self.client as c:
            with self.app_context:
                role_1_id = self.role.save_to_db().id
                role_2_id = self.role_2.save_to_db().id

                results = c.get(
                    f"/roles",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["roles"]), 2)
                self.assertEqual(data["roles"][0]["id"], role_1_id)
                self.assertEqual(data["roles"][1]["id"], role_2_id)

    def test_get_roles_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/roles",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: No roles found.",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
