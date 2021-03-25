import unittest

from werkzeug.security import check_password_hash

from models.member import MemberModel
from models.permission import PermissionModel
from models.role import RoleModel
from tests.base_test import BaseTest


class TestUser(BaseTest):
    """Test all methods for the UserModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.member.email, "jperez@ppty.com")
            self.assertTrue(
                check_password_hash(self.member.password_hash, "pass")
            )
            self.assertEqual(self.member.mobile_phone, "+50769876543")
            self.assertEqual(self.member.first_name, "Juan")
            self.assertEqual(self.member.last_name, "Pérez")
            self.assertEqual(
                self.member.linkedin_profile,
                "https://linkedin.com/in/juan_perez",
            )
            self.assertEqual(
                self.member.github_profile, "https://github.com/juan_perez"
            )
            self.assertEqual(
                self.member.twitter_profile, "https://twitter.com/juan_perez"
            )
            self.assertEqual(
                self.member.profile_picture,
                "https://ppty.com/img/D6e6lKNRCbb4RXs6.png",
            )
            self.assertTrue(self.member.is_active)
            self.assertEqual(self.member.role_id, 1)

    def test_password_setter(self):
        with self.app_context:
            self.member.password = "new_pass"

            self.assertTrue(self.member.verify_password("new_pass"))

    def test_password_getter(self):
        with self.app_context:
            with self.assertRaises(AttributeError):
                _ = self.member.password

    def test_find_all(self):
        with self.app_context:
            self.role.save_to_db()
            member_id = self.member.save_to_db().id

            members = MemberModel.find_all()

            self.assertEqual(members[0].id, member_id)

    def test_find_by_email(self):
        with self.app_context:
            self.role.save_to_db()
            member_id = self.member.save_to_db().id

            member = MemberModel.find_by_email("jperez@ppty.com")

            self.assertEqual(member.id, member_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role.save_to_db()
            member_id = self.member.save_to_db().id

            member = MemberModel.find_by_id(member_id)

            self.assertEqual(member.email, "jperez@ppty.com")

    def test_get_permissions(self):
        with self.app_context:
            role_id = self.role.save_to_db().id
            permission_id = self.permission.save_to_db().id
            member_id = self.member.save_to_db().id

            role = RoleModel.find_by_id(role_id)
            permission = PermissionModel.find_by_id(permission_id)
            role.permissions.append(permission)
            member = MemberModel.find_by_id(member_id)

            self.assertEqual(
                member.get_permissions(), [permission.permission_name]
            )


if __name__ == "__main__":
    unittest.main()
