import json
import unittest

from tests.base_test import BaseTest
from tests.model_test_data import (
    TEST_KEYNOTE_1,
    TEST_KEYNOTE_2,
    TEST_KEYNOTE_400,
    TEST_MEMBER_1,
)


# noinspection PyArgumentList
class TestKeynoteResource(BaseTest):
    """Test all endpoints for the keynote resource"""

    def test_get_keynote_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()
                keynote_id = self.keynote_1.save_to_db().id

                results = c.get(
                    f"/keynotes/{keynote_id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["keynote"]["title"], "Uso de type hints en Python"
                )
                self.assertEqual(
                    data["keynote"]["description"],
                    "Que son los type hints y por qué debemos usarlos",
                )
                self.assertEqual(data["keynote"]["speaker_id"], 1)
                self.assertEqual(data["keynote"]["meeting_id"], 1)

    def test_get_keynote_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.get(
                    f"/keynotes/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Keynote with id '99' was not found.",
                )

    def test_post_keynote_201(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()

                results = c.post(
                    "/keynotes",
                    data=json.dumps(TEST_KEYNOTE_1),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Keynote created successfully."
                )
                self.assertEqual(
                    data["keynote"]["title"], "Uso de type hints en Python"
                )
                self.assertEqual(
                    data["keynote"]["description"],
                    "Que son los type hints y por qué debemos usarlos",
                )
                self.assertEqual(data["keynote"]["speaker_id"], 1)
                self.assertEqual(data["keynote"]["meeting_id"], 1)

    def test_post_keynote_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()

                results = c.post(
                    "/keynotes",
                    data=json.dumps(TEST_KEYNOTE_400),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertTrue("title" in data["error"])
                self.assertTrue("description" in data["error"])

                results = c.post(
                    "/keynotes",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_keynote_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()
                keynote_id = self.keynote_1.save_to_db().id

                results = c.put(
                    f"/keynotes/{keynote_id}",
                    data=json.dumps(TEST_KEYNOTE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["message"], "Keynote modified successfully."
                )
                self.assertEqual(
                    data["keynote"]["title"], "Creando pruebas con UnitTest"
                )
                self.assertEqual(
                    data["keynote"]["description"],
                    "Cómo usar UnitTest para control de calidad de la código",
                )
                self.assertEqual(data["keynote"]["speaker_id"], 1)
                self.assertEqual(data["keynote"]["meeting_id"], 1)

    def test_put_keynote_400(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()
                keynote_id = self.keynote_1.save_to_db().id

                results = c.put(
                    f"/keynotes/{keynote_id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                self.assertEqual(results.status, "400 BAD REQUEST")

    def test_put_keynote_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.put(
                    f"/keynotes/99",
                    data=json.dumps(TEST_KEYNOTE_2),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Keynote with id '99' was not found.",
                )

    def test_delete_keynote_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()
                keynote_id = self.keynote_1.save_to_db().id

                results = c.delete(
                    f"/keynotes/{keynote_id}",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["keynote"]["title"], "Uso de type hints en Python"
                )
                self.assertEqual(
                    data["message"], "Keynote deleted successfully."
                )

    def test_delete_keynote_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])

                results = c.delete(
                    f"/keynotes/99",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: Keynote with id '99' was not found.",
                )

    def test_get_keynotes_200(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                self.speaker_1.save_to_db()
                self.meeting_1.save_to_db()
                keynote_1_id = self.keynote_1.save_to_db().id
                keynote_2_id = self.keynote_2.save_to_db().id

                results = c.get(
                    f"/keynotes",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(len(data["keynotes"]), 2)
                self.assertEqual(data["keynotes"][0]["id"], keynote_1_id)
                self.assertEqual(data["keynotes"][1]["id"], keynote_2_id)

    def test_get_keynotes_404(self):
        with self.client as c:
            with self.app_context:
                self.add_permissions_to_admin()
                member = self.member_1.save_to_db()
                login = self.login(c, member.email, TEST_MEMBER_1["password"])
                
                results = c.get(
                    f"/keynotes",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {login['access_token']}",
                    },
                )

                data = json.loads(results.data)

                self.assertEqual(
                    data["error"],
                    "404 Not Found: No keynotes found.",
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
