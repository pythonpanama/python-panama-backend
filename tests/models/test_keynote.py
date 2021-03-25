import unittest

from models.keynote import KeynoteModel
from tests.base_test import BaseTest


class TestKeynote(BaseTest):
    """Test all methods for the KeynoteModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.keynote.title, "Uso de type hints en Python")
            self.assertEqual(
                self.keynote.description,
                "Que son los type hints y por qué debemos usarlos",
            )
            self.assertEqual(self.keynote.speaker_id, 1)
            self.assertEqual(self.keynote.meeting_id, 1)

    def test_find_all(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            self.speaker.save_to_db()
            self.meeting.save_to_db()
            keynote_id = self.keynote.save_to_db().id

            keynotes = KeynoteModel.find_all()

            self.assertEqual(keynotes[0].id, keynote_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            self.speaker.save_to_db()
            self.meeting.save_to_db()
            keynote_id = self.keynote.save_to_db().id

            keynote = KeynoteModel.find_by_id(keynote_id)

            self.assertEqual(keynote.title, "Uso de type hints en Python")

    def test_find_by_meeting_id(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            self.speaker.save_to_db()
            meeting_id = self.meeting.save_to_db().id
            keynote_id = self.keynote.save_to_db().id

            keynotes = KeynoteModel.find_by_meeting_id(meeting_id)

            self.assertEqual(keynotes[0].id, keynote_id)

    def test_find_by_speaker_id(self):
        with self.app_context:
            self.role.save_to_db()
            self.member.save_to_db()
            self.meeting.save_to_db()
            speaker_id = self.speaker.save_to_db().id
            keynote_id = self.keynote.save_to_db().id

            keynotes = KeynoteModel.find_by_speaker_id(speaker_id)

            self.assertEqual(keynotes[0].id, keynote_id)


if __name__ == "__main__":
    unittest.main()
