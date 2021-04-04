import unittest

from models.speaker import SpeakerModel
from tests.base_test import BaseTest


class TestSpeaker(BaseTest):
    """Test all methods for the SpeakerModel"""

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.speaker_1.first_name, "Tomás")
            self.assertEqual(self.speaker_1.last_name, "González")
            self.assertEqual(self.speaker_1.email, "tgonz@python.org")
            self.assertEqual(
                self.speaker_1.linkedin_profile,
                "https://linkedin.com/in/tomas_gonzalez",
            )
            self.assertEqual(
                self.speaker_1.github_profile,
                "https://github.com/tomas_gonzalez",
            )
            self.assertEqual(
                self.speaker_1.twitter_profile,
                "https://twitter.com/tomas_gonzalez",
            )
            self.assertEqual(
                self.speaker_1.bio, "Experto en Python y el uso de type hints"
            )
            self.assertEqual(
                self.speaker_1.profile_picture,
                "https://ppty.com/img/hA4oCfR&o17mqsXm.png",
            )

    def test_find_all(self):
        with self.app_context:
            speaker_id = self.speaker_1.save_to_db().id

            speakers = SpeakerModel.find_all()

            self.assertEqual(speakers[0].id, speaker_id)

    def test_find_by_email(self):
        with self.app_context:
            speaker_email = self.speaker_1.save_to_db().email

            speaker = SpeakerModel.find_by_email(speaker_email)

            self.assertEqual(speaker.email, "tgonz@python.org")

    def test_find_by_id(self):
        with self.app_context:
            speaker_id = self.speaker_1.save_to_db().id

            speaker = SpeakerModel.find_by_id(speaker_id)

            self.assertEqual(speaker.first_name, "Tomás")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
