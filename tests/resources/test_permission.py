import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_PERMISSION,
    TEST_PERMISSION_2,
    TEST_PERMISSION_400,
)


# noinspection PyArgumentList
class TestPermissionResource(BaseTest):
    """Test all endpoints for the permission resource"""

    def test_get_permission_200(self):
        with self.client as c:
            with self.app_context:
                permission_id = self.permission.save_to_db().id

                results = c.get(
                    f"/permissions/{permission_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["permission"]["permission_name"], "post:project"
                )

    def test_get_permission_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/permissions/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Permission with id '99' was not found.",
                )

    def test_post_permission_201(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/permissions",
                    data=json.dumps(TEST_PERMISSION),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["permission"]["permission_name"], "post:project"
                )

    def test_post_permission_400(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/permissions",
                    data=json.dumps(TEST_PERMISSION_400),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertTrue("permission_name" in data["error"])

    def test_post_permission_409(self):
        with self.client as c:
            with self.app_context:
                self.permission.save_to_db()

                results = c.post(
                    "/permissions",
                    data=json.dumps(TEST_PERMISSION),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Permission with permission_name "
                    "'post:project' already exists.",
                )

    def test_put_permission_200(self):
        with self.client as c:
            with self.app_context:
                permission_id = self.permission.save_to_db().id

                results = c.put(
                    f"/permissions/{permission_id}",
                    data=json.dumps(TEST_PERMISSION_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["permission"]["permission_name"], "post:meeting"
                )

    def test_put_permission_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/permissions/99",
                    data=json.dumps(TEST_PERMISSION_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Permission with id '99' was not found.",
                )

    def test_put_permission_409(self):
        with self.client as c:
            with self.app_context:
                self.permission.save_to_db()
                permission_id = self.permission_2.save_to_db().id

                results = c.put(
                    f"/permissions/{permission_id}",
                    data=json.dumps(TEST_PERMISSION),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Permission with permission_name "
                    "'post:project' already exists.",
                )

    def test_delete_permission_200(self):
        with self.client as c:
            with self.app_context:
                permission_id = self.permission.save_to_db().id

                results = c.delete(
                    f"/permissions/{permission_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["permission"]["permission_name"], "post:project"
                )

    def test_delete_permission_404(self):
        with self.client as c:
            with self.app_context:
                results = c.delete(
                    f"/permissions/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Permission with id '99' was not found.",
                )

    def test_get_permissions_200(self):
        with self.client as c:
            with self.app_context:
                permission_1_id = self.permission.save_to_db().id
                permission_2_id = self.permission_2.save_to_db().id

                results = c.get(
                    f"/permissions",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["permissions"]), 2)
                self.assertEqual(data["permissions"][0]["id"], permission_2_id)
                self.assertEqual(data["permissions"][1]["id"], permission_1_id)

    def test_get_permissions_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/permissions",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: No permissions found.",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
