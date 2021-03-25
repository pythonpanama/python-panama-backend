import unittest

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


if __name__ == "__main__":
    unittest.main()
