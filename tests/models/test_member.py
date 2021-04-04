import unittest

from werkzeug.security import check_password_hash

from models.member import MemberModel
from models.permission import PermissionModel
from models.role import RoleModel
from tests.base_test import BaseTest


class TestMember(BaseTest):
    """Test all methods for the MemberModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.member_1.email, "jperez@ppty.com")
            self.assertTrue(
                check_password_hash(self.member_1.password_hash, "pass")
            )
            self.assertEqual(self.member_1.mobile_phone, "+50769876543")
            self.assertEqual(self.member_1.first_name, "Juan")
            self.assertEqual(self.member_1.last_name, "Pérez")
            self.assertEqual(
                self.member_1.linkedin_profile,
                "https://linkedin.com/in/juan_perez",
            )
            self.assertEqual(
                self.member_1.github_profile, "https://github.com/juan_perez"
            )
            self.assertEqual(
                self.member_1.twitter_profile, "https://twitter.com/juan_perez"
            )
            self.assertEqual(
                self.member_1.profile_picture,
                "https://ppty.com/img/D6e6lKNRCbb4RXs6.png",
            )
            self.assertTrue(self.member_1.is_active)
            self.assertEqual(self.member_1.role_id, 1)

    def test_password_setter(self):
        with self.app_context:
            self.member_1.password = "new_pass"

            self.assertTrue(self.member_1.verify_password("new_pass"))

    def test_password_getter(self):
        with self.app_context:
            with self.assertRaises(AttributeError):
                _ = self.member_1.password

    def test_find_all(self):
        with self.app_context:
            self.role_1.save_to_db()
            member_id = self.member_1.save_to_db().id

            members = MemberModel.find_all()

            self.assertEqual(members[0].id, member_id)

    def test_find_by_email(self):
        with self.app_context:
            self.role_1.save_to_db()
            member_id = self.member_1.save_to_db().id

            member = MemberModel.find_by_email("jperez@ppty.com")

            self.assertEqual(member.id, member_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            member_id = self.member_1.save_to_db().id

            member = MemberModel.find_by_id(member_id)

            self.assertEqual(member.email, "jperez@ppty.com")

    def test_get_permissions(self):
        with self.app_context:
            role_id = self.role_1.save_to_db().id
            permission_id = self.permission_1.save_to_db().id
            member_id = self.member_1.save_to_db().id

            role = RoleModel.find_by_id(role_id)
            permission = PermissionModel.find_by_id(permission_id)
            role.permissions.append(permission)
            member = MemberModel.find_by_id(member_id)

            self.assertEqual(
                member.get_permissions(), [permission.permission_name]
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
