import unittest

from models.permission import PermissionModel
from tests.base_test import BaseTest


class TestPermission(BaseTest):
    """Test all methods for the PermissionModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.permission_1.permission_name, "post:keynote")

    def test_find_by_id(self):
        with self.app_context:
            permission_id = self.permission_1.save_to_db().id

            permission = PermissionModel.find_by_id(permission_id)

            self.assertEqual(permission.permission_name, "post:keynote")

    def test_find_by_name(self):
        with self.app_context:
            permission_id = self.permission_1.save_to_db().id

            permission = PermissionModel.find_by_name("post:keynote")

            self.assertEqual(permission.id, permission_id)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
