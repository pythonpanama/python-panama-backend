import unittest

from models.meeting import MeetingModel
from tests.base_test import BaseTest


class TestMeeting(BaseTest):
    """Test all methods for the MeetingModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.meeting.datetime, "2021-03-31 20:00:00")
            self.assertEqual(self.meeting.type, "online")
            self.assertEqual(
                self.meeting.location,
                "https://www.meetup.com/Python-Panama/events/276661559",
            )
            self.assertEqual(self.meeting.description, "Python Meetup Vol. 25")
            self.assertEqual(self.meeting.creator_id, 1)

    def test_find_all(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            meeting_id = self.meeting.save_to_db().id

            meetings = MeetingModel.find_all()

            self.assertEqual(meetings[0].id, meeting_id)

    def test_find_by_creator_id(self):
        with self.app_context:
            self.role.save_to_db()
            creator_id = self.member.save_to_db().id
            meeting_id = self.meeting.save_to_db().id

            meetings = MeetingModel.find_by_creator_id(creator_id)

            self.assertEqual(meetings[0].id, meeting_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            meeting_id = self.meeting.save_to_db().id

            meeting = MeetingModel.find_by_id(meeting_id)

            self.assertEqual(meeting.description, "Python Meetup Vol. 25")


if __name__ == "__main__": # pragma: no cover
    unittest.main()
