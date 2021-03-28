import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_MEETING,
    TEST_MEETING_2,
    TEST_MEETING_400,
)


# noinspection PyArgumentList
class TestMeetingResource(BaseTest):
    """Test all endpoints for the meeting resource"""

    def test_get_meeting_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                meeting_id = self.meeting.save_to_db().id

                results = c.get(
                    f"/meetings/{meeting_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["meeting"]["datetime"], "2021-03-31T20:00:00"
                )
                self.assertEqual(data["meeting"]["type"], "online")
                self.assertEqual(
                    data["meeting"]["location"],
                    "https://www.meetup.com/Python-Panama/events/276661559",
                )
                self.assertEqual(
                    data["meeting"]["description"],
                    "Python Meetup Vol. 25",
                )
                self.assertEqual(data["meeting"]["creator_id"], 1)

    def test_get_meeting_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/meetings/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Meeting with id '99' was not found.",
                )

    def test_post_meeting_201(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()

                results = c.post(
                    "/meetings",
                    data=json.dumps(TEST_MEETING),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["meeting"]["datetime"], "2021-03-31T20:00:00"
                )
                self.assertEqual(data["meeting"]["type"], "online")
                self.assertEqual(
                    data["meeting"]["location"],
                    "https://www.meetup.com/Python-Panama/events/276661559",
                )
                self.assertEqual(
                    data["meeting"]["description"],
                    "Python Meetup Vol. 25",
                )
                self.assertEqual(data["meeting"]["creator_id"], 1)

    def test_post_meeting_400(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()

                results = c.post(
                    "/meetings",
                    data=json.dumps(TEST_MEETING_400),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertTrue("datetime" in data["error"])
                self.assertTrue("type" in data["error"])
                self.assertTrue("location" in data["error"])
                self.assertTrue("description" in data["error"])

    def test_put_meeting_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                meeting_id = self.meeting.save_to_db().id

                results = c.put(
                    f"/meetings/{meeting_id}",
                    data=json.dumps(TEST_MEETING_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["meeting"]["datetime"], "2021-04-15T20:00:00"
                )
                self.assertEqual(data["meeting"]["type"], "online")
                self.assertEqual(
                    data["meeting"]["location"],
                    "https://www.meetup.com/Python-Panama/events/276661571",
                )
                self.assertEqual(
                    data["meeting"]["description"],
                    "Python Meetup Vol. 26",
                )
                self.assertEqual(data["meeting"]["creator_id"], 1)

    def test_put_meeting_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/meetings/99",
                    data=json.dumps(TEST_MEETING_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Meeting with id '99' was not found.",
                )

    def test_delete_meeting_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                meeting_id = self.meeting.save_to_db().id

                results = c.delete(
                    f"/meetings/{meeting_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["meeting"]["description"], "Python Meetup Vol. 25"
                )
                self.assertEqual(
                    data["message"], "Meeting deleted successfully."
                )

    def test_delete_meeting_404(self):
        with self.client as c:
            with self.app_context:
                results = c.delete(
                    f"/meetings/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Meeting with id '99' was not found.",
                )

    def test_get_meetings_200(self):
        with self.client as c:
            with self.app_context:
                self.role.save_to_db()
                self.member.save_to_db()
                meeting_1_id = self.meeting.save_to_db().id
                meeting_2_id = self.meeting_2.save_to_db().id

                results = c.get(
                    f"/meetings",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["meetings"]), 2)
                self.assertEqual(data["meetings"][0]["id"], meeting_2_id)
                self.assertEqual(data["meetings"][1]["id"], meeting_1_id)

    def test_get_meetings_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/meetings",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: No meetings found.",
                )


if __name__ == "__main__": # pragma: no cover
    unittest.main()
