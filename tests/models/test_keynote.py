import unittest

from models.keynote import KeynoteModel
from tests.base_test import BaseTest
from tests.model_test_data import TEST_KEYNOTE_1


class TestKeynote(BaseTest):
    """Test all methods for the KeynoteModel"""

    TITLE = TEST_KEYNOTE_1["title"]
    DESCRIPTION = TEST_KEYNOTE_1["description"]
    SPEAKER_ID = TEST_KEYNOTE_1["speaker_id"]
    MEETING_ID = TEST_KEYNOTE_1["meeting_id"]

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.keynote_1.title, self.TITLE)
            self.assertEqual(self.keynote_1.description, self.DESCRIPTION)
            self.assertEqual(self.keynote_1.speaker_id, self.SPEAKER_ID)
            self.assertEqual(self.keynote_1.meeting_id, self.MEETING_ID)

    def test_find_all(self):
        with self.app_context:
            keynote, _, _, _, _ = self.add_keynote_to_db(
                self.keynote_1,
                self.role_1,
                self.member_1,
                self.speaker_1,
                self.meeting_1,
            )

            keynotes = KeynoteModel.find_all()

            self.assertEqual(keynotes[0].id, keynote.id)

    def test_find_by_id(self):
        with self.app_context:
            keynote, _, _, _, _ = self.add_keynote_to_db(
                self.keynote_1,
                self.role_1,
                self.member_1,
                self.speaker_1,
                self.meeting_1,
            )

            keynote = KeynoteModel.find_by_id(keynote.id)

            self.assertEqual(keynote.title, self.TITLE)

    def test_find_by_meeting_id(self):
        with self.app_context:
            keynote, _, _, _, meeting = self.add_keynote_to_db(
                self.keynote_1,
                self.role_1,
                self.member_1,
                self.speaker_1,
                self.meeting_1,
            )

            keynotes = KeynoteModel.find_by_meeting_id(meeting.id)

            self.assertEqual(keynotes[0].id, keynote.id)

    def test_find_by_speaker_id(self):
        with self.app_context:
            keynote, _, _, speaker, _ = self.add_keynote_to_db(
                self.keynote_1,
                self.role_1,
                self.member_1,
                self.speaker_1,
                self.meeting_1,
            )

            keynotes = KeynoteModel.find_by_speaker_id(speaker.id)
            print(keynote.meeting.id)
            print(keynote.speaker.id)

            self.assertEqual(keynotes[0].id, keynote.id)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
