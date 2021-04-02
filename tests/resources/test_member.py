import json
import unittest

from flask_jwt_extended import decode_token

from models.member import MemberModel
from models.token import TokenModel
from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEMBER,
    TEST_MEMBER_2,
    TEST_MEMBER_400,
)


# noinspection PyArgumentList
class TestMemberResource(BaseTest):
    """Test all endpoints for the member resource"""

    def test_login_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)
                member_id = self.member.save_to_db().id

                results = c.post(
                    f"/members/login",
                    data=json.dumps(
                        {
                            "email": TEST_MEMBER["email"],
                            "password": TEST_MEMBER["password"],
                        }
                    ),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                member = TEST_MEMBER.copy()
                member["id"] = member_id
                member.pop("password")
                tokens = TokenModel.find_by_member_id(member_id)

                self.assertDictEqual(data["member"], member)
                self.assertEqual(
                    decode_token(data["access_token"])["jti"], tokens[0].jti
                )
                self.assertEqual(
                    decode_token(data["refresh_token"])["jti"], tokens[1].jti
                )

    def test_login_400(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    f"/members/login",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_login_401(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    f"/members/login",
                    data=json.dumps(
                        {
                            "email": TEST_MEMBER["email"],
                            "password": TEST_MEMBER["password"],
                        }
                    ),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "401 UNAUTHORIZED")

    def test_logout_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)
                member = self.member.save_to_db()
                member_id = member.id
                login = self.login(c, member.email, TEST_MEMBER["password"])

                results = c.get(
                    f"/members/logout",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)
                tokens = TokenModel.find_by_member_id(member_id)

                self.assertTrue(tokens[0].revoke)
                self.assertTrue(tokens[1].revoke)

    def test_logout_401(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/members/logout",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(results.status, "401 UNAUTHORIZED")
                self.assertTrue(data["msg"], "Missing Authorization Header")

    def test_get_member_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)
                member_id = self.member.save_to_db().id

                results = c.get(
                    f"/members/{member_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["member"]["email"], "jperez@ppty.com")
                self.assertEqual(
                    data["member"]["mobile_phone"], "+50769876543"
                )
                self.assertEqual(data["member"]["first_name"], "Juan")
                self.assertEqual(data["member"]["last_name"], "Pérez")
                self.assertEqual(
                    data["member"]["linkedin_profile"],
                    "https://linkedin.com/in/juan_perez",
                )
                self.assertEqual(
                    data["member"]["github_profile"],
                    "https://github.com/juan_perez",
                )
                self.assertEqual(
                    data["member"]["twitter_profile"],
                    "https://twitter.com/juan_perez",
                )
                self.assertEqual(
                    data["member"]["profile_picture"],
                    "https://ppty.com/img/D6e6lKNRCbb4RXs6.png",
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertEqual(data["member"]["role_id"], 1)
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_get_member_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/members/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Member with id '99' was not found.",
                )

    def test_post_member_201(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)

                results = c.post(
                    "/members",
                    data=json.dumps(TEST_MEMBER),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Member created successfully."
                )
                self.assertEqual(data["member"]["id"], 1)
                self.assertEqual(data["member"]["email"], "jperez@ppty.com")
                self.assertEqual(
                    data["member"]["mobile_phone"], "+50769876543"
                )
                self.assertEqual(data["member"]["first_name"], "Juan")
                self.assertEqual(data["member"]["last_name"], "Pérez")
                self.assertEqual(
                    data["member"]["linkedin_profile"],
                    "https://linkedin.com/in/juan_perez",
                )
                self.assertEqual(
                    data["member"]["github_profile"],
                    "https://github.com/juan_perez",
                )
                self.assertEqual(
                    data["member"]["twitter_profile"],
                    "https://twitter.com/juan_perez",
                )
                self.assertEqual(
                    data["member"]["profile_picture"],
                    "https://ppty.com/img/D6e6lKNRCbb4RXs6.png",
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertEqual(data["member"]["role_id"], 1)
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_post_member_400(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/members",
                    data=json.dumps(TEST_MEMBER_400),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertTrue("email" in data["error"])
                self.assertTrue("password" in data["error"])
                self.assertTrue("first_name" in data["error"])
                self.assertTrue("last_name" in data["error"])
                self.assertTrue("role_id" in data["error"])

                results = c.post(
                    "/members",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_post_member_409(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)

                self.member.save_to_db()

                results = c.post(
                    "/members",
                    data=json.dumps(TEST_MEMBER),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Member with email "
                    "'jperez@ppty.com' already exists.",
                )

    def test_put_member_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)

                member_id = self.member.save_to_db().id

                results = c.put(
                    f"/members/{member_id}",
                    data=json.dumps(TEST_MEMBER_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Member modified successfully."
                )
                self.assertEqual(data["member"]["id"], 1)
                self.assertEqual(data["member"]["email"], "lcohen@ppty.com")
                self.assertEqual(
                    data["member"]["mobile_phone"], "+50768765432"
                )
                self.assertEqual(data["member"]["first_name"], "Luis")
                self.assertEqual(data["member"]["last_name"], "Cohen")
                self.assertEqual(
                    data["member"]["linkedin_profile"],
                    "https://linkedin.com/in/luis_cohen",
                )
                self.assertEqual(
                    data["member"]["github_profile"],
                    "https://github.com/luis_cohen",
                )
                self.assertEqual(
                    data["member"]["twitter_profile"],
                    "https://twitter.com/luis_cohen",
                )
                self.assertEqual(
                    data["member"]["profile_picture"],
                    "https://ppty.com/img/D6e6lKNRCbblCoH3n.png",
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertEqual(data["member"]["role_id"], 1)
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_put_member_400(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)
                member_id = self.member.save_to_db().id

                results = c.put(
                    f"/members/{member_id}",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_member_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/members/99",
                    data=json.dumps(TEST_MEMBER_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Member with id '99' was not found.",
                )

    def test_put_member_409(self):
        with self.client as c:
            with self.app_context:
                self.permission.save_to_db()
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)
                self.member.save_to_db()
                member_id = self.member_2.save_to_db().id

                results = c.put(
                    f"/members/{member_id}",
                    data=json.dumps(TEST_MEMBER),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "409 Conflict: Member with email "
                    "'jperez@ppty.com' already exists.",
                )

    def test_activate_member_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)

                member_id = self.member.save_to_db().id

                results = c.put(
                    f"/members/{member_id}/activate",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Member activated successfully."
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_activate_member_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/members/99/activate",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Member with id '99' was not found.",
                )

    def test_deactivate_member_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)

                member_id = self.member.save_to_db().id

                results = c.put(
                    f"/members/{member_id}/deactivate",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Member deactivated successfully."
                )
                self.assertFalse(data["member"]["is_active"])
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_deactivate_member_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/members/99/deactivate",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Member with id '99' was not found.",
                )

    def test_change_member_password_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)

                member_id = self.member.save_to_db().id

                results = c.put(
                    f"/members/{member_id}/change_password",
                    data=json.dumps({"password": "new_pass"}),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"],
                    "Member password was modified successfully.",
                )
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

                member = MemberModel.find_by_id(member_id)
                self.assertTrue(member.verify_password("new_pass"))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
