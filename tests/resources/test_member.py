import json
import unittest

from flask_jwt_extended import decode_token

from models.token import TokenModel
from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEMBER_1,
    TEST_MEMBER_2,
    TEST_MEMBER_400,
)


# noinspection PyArgumentList,DuplicatedCode
class TestMemberResource(BaseTest):
    """Test all endpoints for the member resource"""

    EMAIL_1 = TEST_MEMBER_1["email"]
    PASSWORD_1 = TEST_MEMBER_1["password"]
    NEW_PASSWORD_1 = "new_pass"
    MOBILE_PHONE_1 = TEST_MEMBER_1["mobile_phone"]
    FIRST_NAME_1 = TEST_MEMBER_1["first_name"]
    LAST_NAME_1 = TEST_MEMBER_1["last_name"]
    LINKEDIN_PROFILE_1 = TEST_MEMBER_1["linkedin_profile"]
    GITHUB_PROFILE_1 = TEST_MEMBER_1["github_profile"]
    TWITTER_PROFILE_1 = TEST_MEMBER_1["twitter_profile"]
    PROFILE_PICTURE_1 = TEST_MEMBER_1["profile_picture"]
    IS_ACTIVE_1 = TEST_MEMBER_1["is_active"]
    ROLE_ID_1 = TEST_MEMBER_1["role_id"]
    EMAIL_2 = TEST_MEMBER_2["email"]
    PASSWORD_2 = TEST_MEMBER_2["password"]
    MOBILE_PHONE_2 = TEST_MEMBER_2["mobile_phone"]
    FIRST_NAME_2 = TEST_MEMBER_2["first_name"]
    LAST_NAME_2 = TEST_MEMBER_2["last_name"]
    LINKEDIN_PROFILE_2 = TEST_MEMBER_2["linkedin_profile"]
    GITHUB_PROFILE_2 = TEST_MEMBER_2["github_profile"]
    TWITTER_PROFILE_2 = TEST_MEMBER_2["twitter_profile"]
    PROFILE_PICTURE_2 = TEST_MEMBER_2["profile_picture"]
    IS_ACTIVE_2 = TEST_MEMBER_2["is_active"]
    ROLE_ID_2 = TEST_MEMBER_2["role_id"]
    MSG_200 = "Member modified successfully."
    MSG_201 = "Member created successfully."
    MSG_401 = "401 UNAUTHORIZED"
    MSG_401_PUT = "401 Unauthorized: You can only modify your own data."
    MSG_400 = "400 BAD REQUEST"
    MSG_404 = "404 Not Found: Member with id '99' was not found."
    MSG_404_L = "404 Not Found: No members found."
    MSG_409_1 = (
        f"409 Conflict: Member with email '{TEST_MEMBER_1['email']}' "
        f"already exists."
    )
    MSG_409_2 = (
        f"409 Conflict: Member with email '{TEST_MEMBER_2['email']}' "
        f"already exists."
    )
    MSG_ACT_200 = "Member activated successfully."
    MSG_DEA_200 = "Member deactivated successfully."
    MSG_DEL = "Member deleted successfully."
    MSG_HDR = "Missing Authorization Header"
    MSG_PW_200 = "Member password was modified successfully."

    def test_login_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)

                results = c.post(
                    f"/members/login",
                    data=json.dumps(
                        {
                            "email": self.EMAIL_1,
                            "password": self.PASSWORD_1,
                        }
                    ),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                member_dict = TEST_MEMBER_1.copy()
                member_dict["id"] = member.id
                member_dict.pop("password")
                tokens = TokenModel.find_by_member_id(member.id)

                self.assertDictEqual(data["member"], member_dict)
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

                self.assertEqual(results.status, self.MSG_400)

    def test_refresh_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.post(
                    f"/members/refresh",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['refresh_token']}",
                    },
                )

                data = json.loads(results.data)

                tokens = TokenModel.find_by_member_id(member.id)

                self.assertEqual(
                    decode_token(data["access_token"])["jti"], tokens[1].jti
                )
                self.assertTrue(tokens[0].revoked)

    def test_login_401(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    f"/members/login",
                    data=json.dumps(
                        {
                            "email": self.EMAIL_1,
                            "password": self.PASSWORD_1,
                        }
                    ),
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, self.MSG_401)

    def test_logout_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                c.get(
                    f"/members/logout",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                tokens = TokenModel.find_by_member_id(member.id)

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

                self.assertEqual(results.status, self.MSG_401)
                self.assertTrue(data["msg"], self.MSG_HDR)

    def test_get_member_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.get(
                    f"/members/{member.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["member"]["email"], self.EMAIL_1)
                self.assertEqual(
                    data["member"]["mobile_phone"], self.MOBILE_PHONE_1
                )
                self.assertEqual(
                    data["member"]["first_name"], self.FIRST_NAME_1
                )
                self.assertEqual(data["member"]["last_name"], self.LAST_NAME_1)
                self.assertEqual(
                    data["member"]["linkedin_profile"], self.LINKEDIN_PROFILE_1
                )
                self.assertEqual(
                    data["member"]["github_profile"], self.GITHUB_PROFILE_1
                )
                self.assertEqual(
                    data["member"]["twitter_profile"], self.TWITTER_PROFILE_1
                )
                self.assertEqual(
                    data["member"]["profile_picture"], self.PROFILE_PICTURE_1
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertEqual(data["member"]["role_id"], self.ROLE_ID_1)
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_get_member_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.get(
                    f"/members/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_post_member_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()

                results = c.post(
                    "/members",
                    data=json.dumps(TEST_MEMBER_1),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_201)
                self.assertEqual(data["member"]["id"], 1)
                self.assertEqual(data["member"]["email"], self.EMAIL_1)
                self.assertEqual(
                    data["member"]["mobile_phone"], self.MOBILE_PHONE_1
                )
                self.assertEqual(
                    data["member"]["first_name"], self.FIRST_NAME_1
                )
                self.assertEqual(data["member"]["last_name"], self.LAST_NAME_1)
                self.assertEqual(
                    data["member"]["linkedin_profile"], self.LINKEDIN_PROFILE_1
                )
                self.assertEqual(
                    data["member"]["github_profile"], self.GITHUB_PROFILE_1
                )
                self.assertEqual(
                    data["member"]["twitter_profile"], self.TWITTER_PROFILE_1
                )
                self.assertEqual(
                    data["member"]["profile_picture"], self.PROFILE_PICTURE_1
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertEqual(data["member"]["role_id"], self.ROLE_ID_1)
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

                self.assertEqual(results.status, self.MSG_400)

    def test_post_member_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)

                results = c.post(
                    "/members",
                    data=json.dumps(TEST_MEMBER_1),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_409_1)

    def test_put_member_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member.id}",
                    data=json.dumps(TEST_MEMBER_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_200)
                self.assertEqual(data["member"]["id"], 1)
                self.assertEqual(data["member"]["email"], self.EMAIL_2)
                self.assertEqual(
                    data["member"]["mobile_phone"], self.MOBILE_PHONE_2
                )
                self.assertEqual(
                    data["member"]["first_name"], self.FIRST_NAME_2
                )
                self.assertEqual(data["member"]["last_name"], self.LAST_NAME_2)
                self.assertEqual(
                    data["member"]["linkedin_profile"], self.LINKEDIN_PROFILE_2
                )
                self.assertEqual(
                    data["member"]["github_profile"], self.GITHUB_PROFILE_2
                )
                self.assertEqual(
                    data["member"]["twitter_profile"], self.TWITTER_PROFILE_2
                )
                self.assertEqual(
                    data["member"]["profile_picture"], self.PROFILE_PICTURE_2
                )
                self.assertTrue(data["member"]["is_active"])
                self.assertEqual(data["member"]["role_id"], self.ROLE_ID_2)
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_put_member_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_member_401(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member_1, _ = self.add_member_to_db(self.member_1, self.role_1)
                member_2 = self.member_2.save_to_db()
                login = self.login(c, member_2.email, self.PASSWORD_2)

                results = c.put(
                    f"/members/{member_1.id}",
                    data=json.dumps(TEST_MEMBER_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_401_PUT)

    def test_put_member_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/99",
                    data=json.dumps(TEST_MEMBER_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_put_member_409(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                self.member_2.save_to_db()
                member_1, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member_1.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member_1.id}",
                    data=json.dumps(TEST_MEMBER_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_409_2)

    def test_activate_member_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member.id}/activate",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_ACT_200)
                self.assertTrue(data["member"]["is_active"])
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_activate_member_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/99/activate",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_deactivate_member_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member.id}/deactivate",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_DEA_200)
                self.assertFalse(data["member"]["is_active"])
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)

    def test_deactivate_member_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/99/deactivate",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_change_member_password_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member.id}/change_password",
                    data=json.dumps({"password": self.NEW_PASSWORD_1}),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_PW_200)
                self.assertFalse("password" in data)
                self.assertFalse("password_hash" in data)
                self.assertTrue(member.verify_password("new_pass"))

    def test_change_member_password_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/{member.id}/change_password",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_change_member_password_401(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member_1, _ = self.add_member_to_db(self.member_1, self.role_1)
                member_2 = self.member_2.save_to_db()
                login = self.login(c, member_2.email, self.PASSWORD_2)

                results = c.put(
                    f"/members/{member_1.id}/change_password",
                    data=json.dumps({"password": self.NEW_PASSWORD_1}),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_401_PUT)

    def test_change_member_password_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, self.PASSWORD_1)

                results = c.put(
                    f"/members/99/change_password",
                    data=json.dumps({"password": "new_pass"}),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    self.MSG_404,
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
