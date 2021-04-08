import unittest

from models.meeting import MeetingModel
from models.member import MemberModel
from tests.base_test import BaseTest
from tests.model_test_data import TEST_MEETING_1


class TestMeeting(BaseTest):
    """Test all methods for the MeetingModel"""

    DATETIME = TEST_MEETING_1["datetime"]
    TYPE = TEST_MEETING_1["type"]
    LOCATION = TEST_MEETING_1["location"]
    DESCRIPTION = TEST_MEETING_1["description"]
    CREATOR_ID = TEST_MEETING_1["creator_id"]

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.meeting_1.datetime, self.DATETIME)
            self.assertEqual(self.meeting_1.type, self.TYPE)
            self.assertEqual(self.meeting_1.location, self.LOCATION)
            self.assertEqual(self.meeting_1.description, self.DESCRIPTION)
            self.assertEqual(self.meeting_1.creator_id, self.CREATOR_ID)

    def test_find_all(self):
        with self.app_context:
            meeting, _, _ = self.add_meeting_to_db(
                self.meeting_1, self.member_1, self.role_1
            )

            meetings = MeetingModel.find_all()

            self.assertEqual(meetings[0].id, meeting.id)

    def test_find_by_creator_id(self):
        with self.app_context:
            meeting, creator, _ = self.add_meeting_to_db(
                self.meeting_1, self.member_1, self.role_1
            )

            meetings = MeetingModel.find_by_creator_id(creator.id)

            self.assertEqual(meetings[0].id, meeting.id)

    def test_find_by_id(self):
        with self.app_context:
            meeting, _, _ = self.add_meeting_to_db(
                self.meeting_1, self.member_1, self.role_1
            )

            meeting = MeetingModel.find_by_id(meeting.id)

            self.assertEqual(meeting.description, self.DESCRIPTION)

    def test_meetings_members_relation(self):
        with self.app_context:
            meeting, member, _ = self.add_meeting_to_db(
                self.meeting_1, self.member_1, self.role_1
            )

            meeting = MeetingModel.find_by_id(meeting.id)
            member = MemberModel.find_by_id(member.id)
            meeting.members.append(member)

            self.assertEqual(meeting.members[0].email, member.email)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
