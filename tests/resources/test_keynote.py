import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_KEYNOTE_1,
    TEST_KEYNOTE_2,
    TEST_KEYNOTE_400,
    TEST_MEMBER_1,
)


# noinspection PyArgumentList
class TestKeynoteResource(BaseTest):
    """Test all endpoints for the keynote resource"""

    TITLE_1 = TEST_KEYNOTE_1["title"]
    DESCRIPTION_1 = TEST_KEYNOTE_1["description"]
    SPEAKER_ID_1 = TEST_KEYNOTE_1["speaker_id"]
    MEETING_ID_1 = TEST_KEYNOTE_2["meeting_id"]
    TITLE_2 = TEST_KEYNOTE_2["title"]
    DESCRIPTION_2 = TEST_KEYNOTE_2["description"]
    SPEAKER_ID_2 = TEST_KEYNOTE_2["speaker_id"]
    MEETING_ID_2 = TEST_KEYNOTE_2["meeting_id"]
    MSG_200 = "Keynote modified successfully."
    MSG_201 = "Keynote created successfully."
    MSG_400 = "400 BAD REQUEST"
    MSG_404 = "404 Not Found: Keynote with id '99' was not found."
    MSG_404_M = "404 Not Found: Keynotes with meeting_id '99' was not found."
    MSG_404_L = "404 Not Found: No keynotes found."
    MSG_DEL = "Keynote deleted successfully."

    def test_get_keynote_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote, member, _, _, _ = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes/{keynote.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["keynote"]["title"], self.TITLE_1)
                self.assertEqual(
                    data["keynote"]["description"], self.DESCRIPTION_1
                )
                self.assertEqual(
                    data["keynote"]["speaker_id"], self.SPEAKER_ID_1
                )
                self.assertEqual(
                    data["keynote"]["meeting_id"], self.MEETING_ID_1
                )

    def test_get_keynote_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_get_keynotes_by_meeting_id_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote, member, _, _, meeting = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes/meeting/{meeting.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["keynotes"]), 1)
                self.assertEqual(data["keynotes"][0]["title"], self.TITLE_1)
                self.assertEqual(
                    data["keynotes"][0]["description"], self.DESCRIPTION_1
                )
                self.assertEqual(
                    data["keynotes"][0]["speaker_id"], self.SPEAKER_ID_1
                )
                self.assertEqual(data["keynotes"][0]["meeting_id"], meeting.id)

    def test_get_keynotes_by_meeting_id_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes/meeting/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)
                print(data)
                self.assertEqual(data["error"], self.MSG_404_M)

    def test_post_keynote_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote, member, _, _, _ = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/keynotes",
                    data=json.dumps(TEST_KEYNOTE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_201)
                self.assertEqual(data["keynote"]["title"], self.TITLE_2)
                self.assertEqual(
                    data["keynote"]["description"], self.DESCRIPTION_2
                )
                self.assertEqual(
                    data["keynote"]["speaker_id"], self.SPEAKER_ID_2
                )
                self.assertEqual(
                    data["keynote"]["meeting_id"], self.MEETING_ID_2
                )

    def test_post_keynote_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/keynotes",
                    data=json.dumps(TEST_KEYNOTE_400),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertTrue("title" in data["error"])
                self.assertTrue("description" in data["error"])

                results = c.post(
                    "/keynotes",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_keynote_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote, member, _, _, _ = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/keynotes/{keynote.id}",
                    data=json.dumps(TEST_KEYNOTE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_200)
                self.assertEqual(data["keynote"]["title"], self.TITLE_2)
                self.assertEqual(
                    data["keynote"]["description"], self.DESCRIPTION_2
                )
                self.assertEqual(
                    data["keynote"]["speaker_id"], self.SPEAKER_ID_2
                )
                self.assertEqual(
                    data["keynote"]["meeting_id"], self.MEETING_ID_2
                )

    def test_put_keynote_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote, member, _, _, _ = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/keynotes/{keynote.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_keynote_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/keynotes/99",
                    data=json.dumps(TEST_KEYNOTE_2),
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

    def test_delete_keynote_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote, member, _, _, _ = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/keynotes/{keynote.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["keynote"]["title"], self.TITLE_1)
                self.assertEqual(data["message"], self.MSG_DEL)

    def test_delete_keynote_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/keynotes/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_get_keynotes_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                keynote_1, member, _, _, _ = self.add_keynote_to_db(
                    self.keynote_1,
                    self.role_1,
                    self.member_1,
                    self.speaker_1,
                    self.meeting_1,
                )
                keynote_2 = self.keynote_2.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["keynotes"]), 2)
                self.assertEqual(data["keynotes"][0]["id"], keynote_1.id)
                self.assertEqual(data["keynotes"][1]["id"], keynote_2.id)

    def test_get_keynotes_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404_L)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
