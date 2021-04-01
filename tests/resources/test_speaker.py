import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_SPEAKER,
    TEST_SPEAKER_2,
    TEST_SPEAKER_400,
)


# noinspection PyArgumentList
class TestSpeakerResource(BaseTest):
    """Test all endpoints for the speaker resource"""

    def test_get_speaker_200(self):
        with self.client as c:
            with self.app_context:
                speaker_id = self.speaker.save_to_db().id

                results = c.get(
                    f"/speakers/{speaker_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["speaker"]["first_name"], "Tomás")
                self.assertEqual(data["speaker"]["last_name"], "González")
                self.assertEqual(data["speaker"]["email"], "tgonz@python.org")
                self.assertEqual(
                    data["speaker"]["linkedin_profile"],
                    "https://linkedin.com/in/tomas_gonzalez",
                )
                self.assertEqual(
                    data["speaker"]["github_profile"],
                    "https://github.com/tomas_gonzalez",
                )
                self.assertEqual(
                    data["speaker"]["twitter_profile"],
                    "https://twitter.com/tomas_gonzalez",
                )
                self.assertEqual(
                    data["speaker"]["bio"],
                    "Experto en Python y el uso de type hints",
                )
                self.assertEqual(
                    data["speaker"]["profile_picture"],
                    "https://ppty.com/img/hA4oCfR&o17mqsXm.png",
                )

    def test_get_speaker_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/speakers/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Speaker with id '99' was not found.",
                )

    def test_post_speaker_201(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/speakers",
                    data=json.dumps(TEST_SPEAKER),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Speaker created successfully."
                )
                self.assertEqual(data["speaker"]["first_name"], "Tomás")
                self.assertEqual(data["speaker"]["last_name"], "González")
                self.assertEqual(data["speaker"]["email"], "tgonz@python.org")
                self.assertEqual(
                    data["speaker"]["linkedin_profile"],
                    "https://linkedin.com/in/tomas_gonzalez",
                )
                self.assertEqual(
                    data["speaker"]["github_profile"],
                    "https://github.com/tomas_gonzalez",
                )
                self.assertEqual(
                    data["speaker"]["twitter_profile"],
                    "https://twitter.com/tomas_gonzalez",
                )
                self.assertEqual(
                    data["speaker"]["bio"],
                    "Experto en Python y el uso de type hints",
                )
                self.assertEqual(
                    data["speaker"]["profile_picture"],
                    "https://ppty.com/img/hA4oCfR&o17mqsXm.png",
                )

    def test_post_speaker_400(self):
        with self.client as c:
            with self.app_context:
                results = c.post(
                    "/speakers",
                    data=json.dumps(TEST_SPEAKER_400),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertTrue("first_name" in data["error"])
                self.assertTrue("last_name" in data["error"])
                self.assertTrue("bio" in data["error"])

                results = c.post(
                    "/speakers",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_speaker_200(self):
        with self.client as c:
            with self.app_context:
                speaker_id = self.speaker.save_to_db().id

                results = c.put(
                    f"/speakers/{speaker_id}",
                    data=json.dumps(TEST_SPEAKER_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Speaker modified successfully."
                )
                self.assertEqual(data["speaker"]["first_name"], "Edgar")
                self.assertEqual(data["speaker"]["last_name"], "Espino")
                self.assertEqual(data["speaker"]["email"], "eespin@python.org")
                self.assertEqual(
                    data["speaker"]["linkedin_profile"],
                    "https://linkedin.com/in/edgar_espino",
                )
                self.assertEqual(
                    data["speaker"]["github_profile"],
                    "https://github.com/edgar_espino",
                )
                self.assertEqual(
                    data["speaker"]["twitter_profile"],
                    "https://twitter.com/edgar_espino",
                )
                self.assertEqual(
                    data["speaker"]["bio"],
                    "Experto en Flask",
                )
                self.assertEqual(
                    data["speaker"]["profile_picture"],
                    "https://ppty.com/img/hA4oCfR&o17K3fOm.png",
                )

    def test_put_speaker_400(self):
        with self.client as c:
            with self.app_context:
                speaker_id = self.speaker.save_to_db().id

                results = c.put(
                    f"/speakers/{speaker_id}",
                    headers={"Content-Type": "application/json"},
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_speaker_404(self):
        with self.client as c:
            with self.app_context:
                results = c.put(
                    f"/speakers/99",
                    data=json.dumps(TEST_SPEAKER_2),
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Speaker with id '99' was not found.",
                )

    def test_delete_speaker_200(self):
        with self.client as c:
            with self.app_context:
                speaker_id = self.speaker.save_to_db().id

                results = c.delete(
                    f"/speakers/{speaker_id}",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(data["speaker"]["first_name"], "Tomás")
                self.assertEqual(
                    data["message"], "Speaker deleted successfully."
                )

    def test_delete_speaker_404(self):
        with self.client as c:
            with self.app_context:
                results = c.delete(
                    f"/speakers/99",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Speaker with id '99' was not found.",
                )

    def test_get_speakers_200(self):
        with self.client as c:
            with self.app_context:
                speaker_1_id = self.speaker.save_to_db().id
                speaker_2_id = self.speaker_2.save_to_db().id

                results = c.get(
                    f"/speakers",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["speakers"]), 2)
                self.assertEqual(data["speakers"][0]["id"], speaker_2_id)
                self.assertEqual(data["speakers"][1]["id"], speaker_1_id)

    def test_get_speakers_404(self):
        with self.client as c:
            with self.app_context:
                results = c.get(
                    f"/speakers",
                    headers={"Content-Type": "application/json"},
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: No speakers found.",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
