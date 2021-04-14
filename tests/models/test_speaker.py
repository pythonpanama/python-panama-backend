import unittest

from models.speaker import SpeakerModel
from tests.base_test import BaseTest
from tests.model_test_data import TEST_SPEAKER_1


class TestSpeaker(BaseTest):
    """Test all methods for the SpeakerModel"""

    FIRST_NAME = TEST_SPEAKER_1["first_name"]
    LAST_NAME = TEST_SPEAKER_1["last_name"]
    EMAIL = TEST_SPEAKER_1["email"]
    LINKEDIN_PROFILE = TEST_SPEAKER_1["linkedin_profile"]
    GITHUB_PROFILE = TEST_SPEAKER_1["github_profile"]
    TWITTER_PROFILE = TEST_SPEAKER_1["twitter_profile"]
    BIO = TEST_SPEAKER_1["bio"]
    PROFILE_PICTURE = TEST_SPEAKER_1["profile_picture"]

    def test_init(self):
        with self.app_context:
            self.assertEqual(self.speaker_1.first_name, self.FIRST_NAME)
            self.assertEqual(self.speaker_1.last_name, self.LAST_NAME)
            self.assertEqual(self.speaker_1.email, self.EMAIL)
            self.assertEqual(
                self.speaker_1.linkedin_profile, self.LINKEDIN_PROFILE
            )
            self.assertEqual(
                self.speaker_1.github_profile, self.GITHUB_PROFILE
            )
            self.assertEqual(
                self.speaker_1.twitter_profile, self.TWITTER_PROFILE
            )
            self.assertEqual(self.speaker_1.bio, self.BIO)
            self.assertEqual(
                self.speaker_1.profile_picture, self.PROFILE_PICTURE
            )

    def test_find_all(self):
        with self.app_context:
            speaker = self.add_speaker_to_db(self.speaker_1)

            speakers = SpeakerModel.find_all()

            self.assertEqual(speakers[0].id, speaker.id)

    def test_find_by_email(self):
        with self.app_context:
            speaker = self.add_speaker_to_db(self.speaker_1)

            speaker = SpeakerModel.find_by_email(speaker.email)

            self.assertEqual(speaker.email, self.EMAIL)

    def test_find_by_id(self):
        with self.app_context:
            speaker = self.add_speaker_to_db(self.speaker_1)

            speaker = SpeakerModel.find_by_id(speaker.id)

            self.assertEqual(speaker.first_name, self.FIRST_NAME)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
