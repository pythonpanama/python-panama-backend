import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEETING_1,
    TEST_MEETING_2,
    TEST_MEETING_400,
    TEST_MEMBER_1,
)


# noinspection PyArgumentList
class TestMeetingResource(BaseTest):
    """Test all endpoints for the meeting resource"""

    DATETIME_1 = TEST_MEETING_1["datetime"].replace(" ", "T")
    TYPE_1 = TEST_MEETING_1["type"]
    LOCATION_1 = TEST_MEETING_1["location"]
    DESCRIPTION_1 = TEST_MEETING_1["description"]
    CREATOR_ID_1 = TEST_MEETING_1["creator_id"]
    DATETIME_2 = TEST_MEETING_2["datetime"].replace(" ", "T")
    TYPE_2 = TEST_MEETING_2["type"]
    LOCATION_2 = TEST_MEETING_2["location"]
    DESCRIPTION_2 = TEST_MEETING_2["description"]
    CREATOR_ID_2 = TEST_MEETING_2["creator_id"]
    MSG_200 = "Meeting modified successfully."
    MSG_201 = "Meeting created successfully."
    MSG_400 = "400 BAD REQUEST"
    MSG_404 = "404 Not Found: Meeting with id '99' was not found."
    MSG_404_L = "404 Not Found: No meetings found."
    MSG_DEL = "Meeting deleted successfully."

    def test_get_meeting_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/meetings/{meeting.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["meeting"]["datetime"], self.DATETIME_1)
                self.assertEqual(data["meeting"]["type"], self.TYPE_1)
                self.assertEqual(data["meeting"]["location"], self.LOCATION_1)
                self.assertEqual(
                    data["meeting"]["description"], self.DESCRIPTION_1
                )
                self.assertEqual(
                    data["meeting"]["creator_id"], self.CREATOR_ID_1
                )

    def test_get_meeting_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                results = c.get(
                    f"/meetings/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_post_meeting_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/meetings",
                    data=json.dumps(TEST_MEETING_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_201)
                self.assertEqual(data["meeting"]["datetime"], self.DATETIME_2)
                self.assertEqual(data["meeting"]["type"], self.TYPE_2)
                self.assertEqual(data["meeting"]["location"], self.LOCATION_2)
                self.assertEqual(
                    data["meeting"]["description"],
                    self.DESCRIPTION_2,
                )
                self.assertEqual(
                    data["meeting"]["creator_id"], self.CREATOR_ID_2
                )

    def test_post_meeting_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.post(
                    "/meetings",
                    data=json.dumps(TEST_MEETING_400),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertTrue("datetime" in data["error"])
                self.assertTrue("type" in data["error"])
                self.assertTrue("location" in data["error"])
                self.assertTrue("description" in data["error"])

                results = c.post(
                    "/meetings",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_meeting_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/meetings/{meeting.id}",
                    data=json.dumps(TEST_MEETING_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["message"], self.MSG_200)
                self.assertEqual(data["meeting"]["datetime"], self.DATETIME_2)
                self.assertEqual(data["meeting"]["type"], self.TYPE_2)
                self.assertEqual(data["meeting"]["location"], self.LOCATION_2)
                self.assertEqual(
                    data["meeting"]["description"], self.DESCRIPTION_2
                )
                self.assertEqual(
                    data["meeting"]["creator_id"], self.CREATOR_ID_2
                )

    def test_put_meeting_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/meetings/{meeting.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, self.MSG_400)

    def test_put_meeting_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/meetings/99",
                    data=json.dumps(TEST_MEETING_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_delete_meeting_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/meetings/{meeting.id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["meeting"]["description"], self.DESCRIPTION_1
                )
                self.assertEqual(data["message"], self.MSG_DEL)

    def test_delete_meeting_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/meetings/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404)

    def test_get_meetings_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                meeting_1, member, _ = self.add_meeting_to_db(
                    self.meeting_1, self.member_1, self.role_1
                )
                meeting_2 = self.meeting_2.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/meetings",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["meetings"]), 2)
                self.assertEqual(data["meetings"][0]["id"], meeting_2.id)
                self.assertEqual(data["meetings"][1]["id"], meeting_1.id)

    def test_get_meetings_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member, _ = self.add_member_to_db(self.member_1, self.role_1)
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/meetings",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(data["error"], self.MSG_404_L)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
