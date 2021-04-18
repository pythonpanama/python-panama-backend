import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEMBER_1,
    TEST_SPEAKER_1,
    TEST_SPEAKER_2,
    TEST_SPEAKER_400,
)


# noinspection PyArgumentList
class TestSpeakerResource(BaseTest):
    """Test all endpoints for the speaker resource"""

    FIRST_NAME_1 = TEST_SPEAKER_1["first_name"]
    LAST_NAME_1 = TEST_SPEAKER_1["last_name"]
    EMAIL_1 = TEST_SPEAKER_1["email"]
    LINKEDIN_PROFILE_1 = TEST_SPEAKER_1["linkedin_profile"]
    GITHUB_PROFILE_1 = TEST_SPEAKER_1["github_profile"]
    TWITTER_PROFILE_1 = TEST_SPEAKER_1["twitter_profile"]
    BIO_1 = TEST_SPEAKER_1["bio"]
    PROFILE_PICTURE_1 = TEST_SPEAKER_1["profile_picture"]
    FIRST_NAME_2 = TEST_SPEAKER_2["first_name"]
    LAST_NAME_2 = TEST_SPEAKER_2["last_name"]
    EMAIL_2 = TEST_SPEAKER_2["email"]
    LINKEDIN_PROFILE_2 = TEST_SPEAKER_2["linkedin_profile"]
    GITHUB_PROFILE_2 = TEST_SPEAKER_2["github_profile"]
    TWITTER_PROFILE_2 = TEST_SPEAKER_2["twitter_profile"]
    BIO_2 = TEST_SPEAKER_2["bio"]
    PROFILE_PICTURE_2 = TEST_SPEAKER_2["profile_picture"]
    MSG_200 = "Speaker modified successfully."
    MSG_201 = "Speaker created successfully."
    MSG_400 = "400 BAD REQUEST"
    MSG_404 = "404 Not Found: Speaker with id '99' was not found."
    MSG_404_L = "404 Not Found: No speakers found."
    MSG_DEL = "Speaker deleted successfully."

    def test_get_speaker_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                speaker = self.add_speaker_to_db(self.speaker_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/speakers/{speaker.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["speaker"]["first_name"], self.FIRST_NAME_1
                )
                self.assertEqual(
                    data["speaker"]["last_name"], self.LAST_NAME_1
                )
                self.assertEqual(data["speaker"]["email"], self.EMAIL_1)
                self.assertEqual(
                    data["speaker"]["linkedin_profile"],
                    self.LINKEDIN_PROFILE_1,
                )
                self.assertEqual(
                    data["speaker"]["github_profile"], self.GITHUB_PROFILE_1
                )
                self.assertEqual(
                    data["speaker"]["twitter_profile"], self.TWITTER_PROFILE_1
                )
                self.assertEqual(data["speaker"]["bio"], self.BIO_1)
                self.assertEqual(
                    data["speaker"]["profile_picture"], self.PROFILE_PICTURE_1
                )

    def test_get_speaker_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/speakers/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_post_speaker_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/speakers",
                    data=json.dumps(TEST_SPEAKER_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_201)
                self.assertEqual(
                    data["speaker"]["first_name"], self.FIRST_NAME_1
                )
                self.assertEqual(
                    data["speaker"]["last_name"], self.LAST_NAME_1
                )
                self.assertEqual(data["speaker"]["email"], self.EMAIL_1)
                self.assertEqual(
                    data["speaker"]["linkedin_profile"],
                    self.LINKEDIN_PROFILE_1,
                )
                self.assertEqual(
                    data["speaker"]["github_profile"], self.GITHUB_PROFILE_1
                )
                self.assertEqual(
                    data["speaker"]["twitter_profile"], self.TWITTER_PROFILE_1
                )
                self.assertEqual(data["speaker"]["bio"], self.BIO_1)
                self.assertEqual(
                    data["speaker"]["profile_picture"], self.PROFILE_PICTURE_1
                )

    def test_post_speaker_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/speakers",
                    data=json.dumps(TEST_SPEAKER_400),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertTrue("first_name" in data["error"])
                self.assertTrue("last_name" in data["error"])
                self.assertTrue("bio" in data["error"])

                results = c.post(
                    "/speakers",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_speaker_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                speaker = self.add_speaker_to_db(self.speaker_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/speakers/{speaker.id}",
                    data=json.dumps(TEST_SPEAKER_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_200)
                self.assertEqual(
                    data["speaker"]["first_name"], self.FIRST_NAME_2
                )
                self.assertEqual(
                    data["speaker"]["last_name"], self.LAST_NAME_2
                )
                self.assertEqual(data["speaker"]["email"], self.EMAIL_2)
                self.assertEqual(
                    data["speaker"]["linkedin_profile"],
                    self.LINKEDIN_PROFILE_2,
                )
                self.assertEqual(
                    data["speaker"]["github_profile"], self.GITHUB_PROFILE_2
                )
                self.assertEqual(
                    data["speaker"]["twitter_profile"], self.TWITTER_PROFILE_2
                )
                self.assertEqual(data["speaker"]["bio"], self.BIO_2)
                self.assertEqual(
                    data["speaker"]["profile_picture"], self.PROFILE_PICTURE_2
                )

    def test_put_speaker_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                speaker = self.add_speaker_to_db(self.speaker_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/speakers/{speaker.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_speaker_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/speakers/99",
                    data=json.dumps(TEST_SPEAKER_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_delete_speaker_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                speaker = self.add_speaker_to_db(self.speaker_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/speakers/{speaker.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["speaker"]["first_name"], self.FIRST_NAME_1
                )
                self.assertEqual(data["message"], self.MSG_DEL)

    def test_delete_speaker_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/speakers/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_get_speakers_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                speaker_1 = self.add_speaker_to_db(self.speaker_1)
                speaker_2 = self.add_speaker_to_db(self.speaker_2)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/speakers",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["speakers"]), 2)
                self.assertEqual(data["speakers"][0]["id"], speaker_2.id)
                self.assertEqual(data["speakers"][1]["id"], speaker_1.id)

    def test_get_speakers_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/speakers",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404_L)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
