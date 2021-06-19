import unittest

from werkzeug.security import check_password_hash

from models.member import MemberModel
from tests.base_test import BaseTest
from tests.model_test_data import TEST_MEMBER_1


class TestMember(BaseTest):
    """Test all methods for the MemberModel"""

    EMAIL = TEST_MEMBER_1["email"]
    PASSWORD = TEST_MEMBER_1["password"]
    NEW_PASSWORD = "new_pass"
    MOBILE_PHONE = TEST_MEMBER_1["mobile_phone"]
    FIRST_NAME = TEST_MEMBER_1["first_name"]
    LAST_NAME = TEST_MEMBER_1["last_name"]
    LINKEDIN_PROFILE = TEST_MEMBER_1["linkedin_profile"]
    GITHUB_PROFILE = TEST_MEMBER_1["github_profile"]
    TWITTER_PROFILE = TEST_MEMBER_1["twitter_profile"]
    PROFILE_PICTURE = TEST_MEMBER_1["profile_picture"]
    IS_ACTIVE = TEST_MEMBER_1["is_active"]
    ROLE_ID = TEST_MEMBER_1["role_id"]

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.member_1.email, self.EMAIL)
            self.assertTrue(
                check_password_hash(self.member_1.password_hash, self.PASSWORD)
            )
            self.assertEqual(self.member_1.mobile_phone, self.MOBILE_PHONE)
            self.assertEqual(self.member_1.first_name, self.FIRST_NAME)
            self.assertEqual(self.member_1.last_name, self.LAST_NAME)
            self.assertEqual(
                self.member_1.linkedin_profile, self.LINKEDIN_PROFILE
            )
            self.assertEqual(self.member_1.github_profile, self.GITHUB_PROFILE)
            self.assertEqual(
                self.member_1.twitter_profile, self.TWITTER_PROFILE
            )
            self.assertEqual(
                self.member_1.profile_picture, self.PROFILE_PICTURE
            )
            self.assertTrue(self.member_1.is_active)
            self.assertEqual(self.member_1.role_id, self.ROLE_ID)

    def test_password_setter(self):
        with self.app_context:
            self.member_1.password = self.NEW_PASSWORD

            self.assertTrue(self.member_1.verify_password(self.NEW_PASSWORD))

    def test_password_getter(self):
        with self.app_context:
            with self.assertRaises(AttributeError):
                _ = self.member_1.password

    def test_find_all(self):
        with self.app_context:
            member, _ = self.add_member_to_db(self.member_1, self.role_1)

            members = MemberModel.find_all()

            self.assertEqual(members[0].id, member.id)

    def test_find_by_email(self):
        with self.app_context:
            member_1, _ = self.add_member_to_db(self.member_1, self.role_1)

            member = MemberModel.find_by_email(self.EMAIL)

            self.assertEqual(member.id, member_1.id)

    def test_find_by_id(self):
        with self.app_context:
            member_1, _ = self.add_member_to_db(self.member_1, self.role_1)

            member = MemberModel.find_by_id(member_1.id)

            self.assertEqual(member.email, self.EMAIL)

    def test_get_permissions(self):
        with self.app_context:
            member_1, role = self.add_member_to_db(self.member_1, self.role_1)
            permission = self.add_permission_to_db(self.permission_1)
            role.permissions.append(permission)

            member = MemberModel.find_by_id(member_1.id)

            self.assertEqual(
                member.get_permissions(), [permission.permission_name]
            )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
