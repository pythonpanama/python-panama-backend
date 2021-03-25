import unittest

from models.permission import PermissionModel
from tests.base_test import BaseTest


class TestPermission(BaseTest):
    """Test all methods for the PermissionModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.permission.permission_name, "post:project")

    def test_find_by_id(self):
        with self.app_context:
            permission_id = self.permission.save_to_db().id

            permission = PermissionModel.find_by_id(permission_id)

            self.assertEqual(permission.permission_name, "post:project")

    def test_find_by_name(self):
        with self.app_context:
            permission_id = self.permission.save_to_db().id

            permission = PermissionModel.find_by_name("post:project")

            self.assertEqual(permission.id, permission_id)


if __name__ == "__main__":
    unittest.main()
