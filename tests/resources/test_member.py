import json
import unittest

from flask_jwt_extended import decode_token

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

                TEST_MEMBER["id"] = member_id
                TEST_MEMBER.pop("password")
                tokens = TokenModel.find_by_member_id(member_id)

                self.assertDictEqual(data["member"], TEST_MEMBER)
                self.assertEqual(
                    decode_token(data["access_token"])["jti"], tokens[0].jti
                )
                self.assertEqual(
                    decode_token(data["refresh_token"])["jti"], tokens[1].jti
                )

    def test_logout_200(self):
        with self.client as c:
            with self.app_context:
                role = self.role.save_to_db()
                permission = self.permission.save_to_db()
                role.permissions.append(permission)
                member = self.member.save_to_db()
                member_id = member.id
                login = self.login(c, member.email, "pass")

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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
