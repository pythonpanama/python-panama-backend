import unittest

from models.meeting import MeetingModel
from models.member import MemberModel
from tests.base_test import BaseTest


class TestMeeting(BaseTest):
    """Test all methods for the MeetingModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.meeting_1.datetime, "2021-03-31 20:00:00")
            self.assertEqual(self.meeting_1.type, "online")
            self.assertEqual(
                self.meeting_1.location,
                "https://www.meetup.com/Python-Panama/events/276661559",
            )
            self.assertEqual(
                self.meeting_1.description, "Python Meetup Vol. 25"
            )
            self.assertEqual(self.meeting_1.creator_id, 1)

    def test_find_all(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            meeting_id = self.meeting_1.save_to_db().id

            meetings = MeetingModel.find_all()

            self.assertEqual(meetings[0].id, meeting_id)

    def test_find_by_creator_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            creator_id = self.member_1.save_to_db().id
            meeting_id = self.meeting_1.save_to_db().id

            meetings = MeetingModel.find_by_creator_id(creator_id)

            self.assertEqual(meetings[0].id, meeting_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            meeting_id = self.meeting_1.save_to_db().id

            meeting = MeetingModel.find_by_id(meeting_id)

            self.assertEqual(meeting.description, "Python Meetup Vol. 25")

    def test_meetings_members_relation(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            meeting_id = self.meeting_1.save_to_db().id
            member_id = self.member_1.save_to_db().id

            meeting = MeetingModel.find_by_id(meeting_id)
            member = MemberModel.find_by_id(member_id)
            meeting.members.append(member)

            self.assertEqual(meeting.members[0].email, "jperez@ppty.com")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
