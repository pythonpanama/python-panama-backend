import unittest

from models.keynote import KeynoteModel
from tests.base_test import BaseTest


class TestKeynote(BaseTest):
    """Test all methods for the KeynoteModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(
                self.keynote_1.title, "Uso de type hints en Python"
            )
            self.assertEqual(
                self.keynote_1.description,
                "Que son los type hints y por qué debemos usarlos",
            )
            self.assertEqual(self.keynote_1.speaker_id, 1)
            self.assertEqual(self.keynote_1.meeting_id, 1)

    def test_find_all(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            self.speaker_1.save_to_db()
            self.meeting_1.save_to_db()
            keynote_id = self.keynote_1.save_to_db().id

            keynotes = KeynoteModel.find_all()

            self.assertEqual(keynotes[0].id, keynote_id)

    def test_find_by_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            self.speaker_1.save_to_db()
            self.meeting_1.save_to_db()
            keynote_id = self.keynote_1.save_to_db().id

            keynote = KeynoteModel.find_by_id(keynote_id)

            self.assertEqual(keynote.title, "Uso de type hints en Python")

    def test_find_by_meeting_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            self.speaker_1.save_to_db()
            meeting_id = self.meeting_1.save_to_db().id
            keynote_id = self.keynote_1.save_to_db().id

            keynotes = KeynoteModel.find_by_meeting_id(meeting_id)

            self.assertEqual(keynotes[0].id, keynote_id)

    def test_find_by_speaker_id(self):
        with self.app_context:
            self.role_1.save_to_db()
            self.member_1.save_to_db()
            self.meeting_1.save_to_db()
            speaker_id = self.speaker_1.save_to_db().id
            keynote_id = self.keynote_1.save_to_db().id

            keynotes = KeynoteModel.find_by_speaker_id(speaker_id)

            self.assertEqual(keynotes[0].id, keynote_id)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
