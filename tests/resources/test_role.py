import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEMBER_1,
    TEST_ROLE_1,
    TEST_ROLE_2,
    TEST_ROLE_400,
)


# noinspection PyArgumentList
class TestRoleResource(BaseTest):
    """Test all endpoints for the role resource"""

    def test_get_role_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/roles/1",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "admin")

    def test_get_role_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/roles/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Role with id '99' was not found.",
                )

    def test_post_role_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], "Role created successfully.")
                self.assertEqual(data["role"]["role_name"], "member")

    def test_post_role_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE_400),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertTrue("role_name" in data["error"])

                results = c.post(
                    "/roles",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_post_role_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
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
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/roles/1",
                    data=json.dumps(TEST_ROLE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Role modified successfully."
                )
                self.assertEqual(data["role"]["role_name"], "member")

    def test_put_role_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/roles/1",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_role_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/roles/99",
                    data=json.dumps(TEST_ROLE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Role with id '99' was not found.",
                )

    def test_put_role_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                role_id = self.role_2.save_to_db().id

                results = c.put(
                    f"/roles/{role_id}",
                    data=json.dumps(TEST_ROLE_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
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
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                role_id = self.role_2.save_to_db().id

                results = c.delete(
                    f"/roles/{role_id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "member")

    def test_delete_role_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/roles/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Role with id '99' was not found.",
                )

    def test_get_roles_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                role_2_id = self.role_2.save_to_db().id

                results = c.get(
                    f"/roles",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["roles"]), 2)
                self.assertEqual(data["roles"][0]["id"], 1)
                self.assertEqual(data["roles"][1]["id"], role_2_id)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
