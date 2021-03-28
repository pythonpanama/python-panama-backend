import unittest

from models.permission import PermissionModel
from models.role import RoleModel
from tests.base_test import BaseTest


class TestRole(BaseTest):
    """Test all methods for the RoleModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.role.role_name, "admin")

    def test_find_by_id(self):
        with self.app_context:
            role_id = self.role.save_to_db().id

            role = RoleModel.find_by_id(role_id)

            self.assertEqual(role.role_name, "admin")

    def test_find_by_name(self):
        with self.app_context:
            role_id = self.role.save_to_db().id

            role = RoleModel.find_by_name("admin")

            self.assertEqual(role.id, role_id)

    def test_role_permission_relation(self):
        with self.app_context:
            role_id = self.role.save_to_db().id
            permission_id = self.permission.save_to_db().id

            role = RoleModel.find_by_id(role_id)
            permission = PermissionModel.find_by_id(permission_id)
            role.permissions.append(permission)

            self.assertEqual(
                role.permissions[0].permission_name, "post:project"
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
