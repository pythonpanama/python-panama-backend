import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEMBER_1,
    TEST_PERMISSION_1,
    TEST_PERMISSION_2,
    TEST_PERMISSION_9,
    TEST_PERMISSION_400,
)


# noinspection PyArgumentList
class TestPermissionResource(BaseTest):
    """Test all endpoints for the permission resource"""

    def test_get_permission_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/permissions/1",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["permission"]["permission_name"], "post:keynote"
                )

    def test_get_permission_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/permissions/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Permission with id '99' was not found.",
                )

    def test_post_permission_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/permissions",
                    data=json.dumps(TEST_PERMISSION_9),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Permission created successfully."
                )
                self.assertEqual(
                    data["permission"]["permission_name"], "post:token"
                )

    def test_post_permission_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/permissions",
                    data=json.dumps(TEST_PERMISSION_400),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertTrue("permission_name" in data["error"])

                results = c.post(
                    "/permissions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_post_permission_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/permissions",
                    data=json.dumps(TEST_PERMISSION_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Permission with permission_name "
                    "'post:keynote' already exists.",
                )

    def test_put_permission_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/permissions/1",
                    data=json.dumps(TEST_PERMISSION_9),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Permission modified successfully."
                )
                self.assertEqual(
                    data["permission"]["permission_name"], "post:token"
                )

    def test_put_permission_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/permissions/1",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_permission_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/permissions/99",
                    data=json.dumps(TEST_PERMISSION_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Permission with id '99' was not found.",
                )

    def test_put_permission_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/permissions/2",
                    data=json.dumps(TEST_PERMISSION_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Permission with permission_name "
                    "'post:keynote' already exists.",
                )

    def test_delete_permission_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/permissions/1",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["permission"]["permission_name"], "post:keynote"
                )

    def test_delete_permission_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/permissions/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Permission with id '99' was not found.",
                )

    def test_get_permissions_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/permissions",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["permissions"]), 8)
                self.assertEqual(data["permissions"][1]["id"], 3)
                self.assertEqual(data["permissions"][0]["id"], 4)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
