import unittest

from models.role import RoleModel
from tests.base_test import BaseTest
from tests.model_test_data import TEST_PERMISSION_1, TEST_ROLE_1


class TestRole(BaseTest):
    """Test all methods for the RoleModel"""

    ROLE_NAME = TEST_ROLE_1["role_name"]
    PERMISSION_NAME = TEST_PERMISSION_1["permission_name"]

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.role_1.role_name, self.ROLE_NAME)

    def test_find_by_id(self):
        with self.app_context:
            role = self.add_role_to_db(self.role_1)

            role = RoleModel.find_by_id(role.id)

            self.assertEqual(role.role_name, self.ROLE_NAME)

    def test_find_by_name(self):
        with self.app_context:
            role_1 = self.add_role_to_db(self.role_1)

            role = RoleModel.find_by_name(self.ROLE_NAME)

            self.assertEqual(role.id, role_1.id)

    def test_role_permission_relation(self):
        with self.app_context:
            role = self.add_role_to_db(self.role_1)
            permission = self.add_permission_to_db(self.permission_1)
            role.permissions.append(permission)

            self.assertEqual(
                role.permissions[0].permission_name, self.PERMISSION_NAME
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
