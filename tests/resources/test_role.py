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

    PASSWORD_1 = TEST_MEMBER_1["password"]
    ROLE_NAME_1 = TEST_ROLE_1["role_name"]
    ROLE_NAME_2 = TEST_ROLE_2["role_name"]
    MSG_200 = "Role modified successfully."
    MSG_201 = "Role created successfully."
    MSG_400 = "400 BAD REQUEST"
    MSG_404 = "404 Not Found: Role with id '99' was not found."
    MSG_409_1 = (
        f"409 Conflict: Role with role_name '{TEST_ROLE_1['role_name']}' "
        f"already exists."
    )
    MSG_DEL = "Role deleted successfully."

    def test_get_role_200(self):
        with self.client as c:
            with self.app_context:
                role = self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_2)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/roles/{role.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], self.ROLE_NAME_1)

    def test_get_role_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_2)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.get(
                    f"/roles/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_post_role_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_201)
                self.assertEqual(data["role"]["role_name"], self.ROLE_NAME_2)

    def test_post_role_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_2)
                login = self.login(c, member.email, self.PASSWORD_1)

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

                self.assertEqual(results.status, self.MSG_400)

    def test_post_role_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_2)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.post(
                    "/roles",
                    data=json.dumps(TEST_ROLE_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_409_1)

    def test_put_role_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/roles/1",
                    data=json.dumps(TEST_ROLE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_200)
                self.assertEqual(data["role"]["role_name"], self.ROLE_NAME_2)

    def test_put_role_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, role = self.add_member_to_db(
                    self.member_1, self.role_2
                )
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/roles/{role.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_role_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_2)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/roles/99",
                    data=json.dumps(TEST_ROLE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_put_role_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, role = self.add_member_to_db(
                    self.member_1, self.role_2
                )
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/roles/{role.id}",
                    data=json.dumps(TEST_ROLE_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_409_1)

    def test_delete_role_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, role = self.add_member_to_db(
                    self.member_1, self.role_2
                )
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.delete(
                    f"/roles/{role.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["role"]["role_name"], "member")
                self.assertEqual(data["message"], self.MSG_DEL)

    def test_delete_role_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_2)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.delete(
                    f"/roles/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_get_roles_200(self):
        with self.client as c:
            with self.app_context:
                role_1 = self.add_permissions_to_admin()
                member, role_2 = self.add_member_to_db(
                    self.member_1, self.role_2
                )
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.get(
                    f"/roles",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["roles"]), 2)
                self.assertEqual(data["roles"][0]["id"], role_1.id)
                self.assertEqual(data["roles"][1]["id"], role_2.id)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
