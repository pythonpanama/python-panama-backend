import json
from unittest import TestCase

from app import create_app, db
from custom_types import LoginJSON
from models.keynote import KeynoteModel
from models.meeting import MeetingModel
from models.member import MemberModel
from models.permission import PermissionModel
from models.project import ProjectModel
from models.role import RoleModel
from models.speaker import SpeakerModel
from tests.model_test_data import (
    TEST_KEYNOTE,
    TEST_KEYNOTE_2,
    TEST_MEMBER,
    TEST_MEMBER_2,
    TEST_MEETING,
    TEST_MEETING_2,
    TEST_PERMISSION,
    TEST_PERMISSION_2,
    TEST_PROJECT,
    TEST_PROJECT_2,
    TEST_ROLE,
    TEST_ROLE_2,
    TEST_SPEAKER,
    TEST_SPEAKER_2,
)

app = create_app("testing")


# noinspection PyArgumentList
class BaseTest(TestCase):
    """Base class which is inherited by all test classes"""

    @classmethod
    def setUpClass(cls) -> None:
        pass

    def setUp(self) -> None:
        """Create all db tables before each test"""
        self.client = app.test_client()
        self.app_context = app.app_context()

        with self.app_context:
            db.create_all()

            self.keynote = KeynoteModel(**TEST_KEYNOTE)
            self.keynote_2 = KeynoteModel(**TEST_KEYNOTE_2)
            self.member = MemberModel(**TEST_MEMBER)
            self.member_2 = MemberModel(**TEST_MEMBER_2)
            self.meeting = MeetingModel(**TEST_MEETING)
            self.meeting_2 = MeetingModel(**TEST_MEETING_2)
            self.permission = PermissionModel(**TEST_PERMISSION)
            self.permission_2 = PermissionModel(**TEST_PERMISSION_2)
            self.project = ProjectModel(**TEST_PROJECT)
            self.project_2 = ProjectModel(**TEST_PROJECT_2)
            self.role = RoleModel(**TEST_ROLE)
            self.role_2 = RoleModel(**TEST_ROLE_2)
            self.speaker = SpeakerModel(**TEST_SPEAKER)
            self.speaker_2 = SpeakerModel(**TEST_SPEAKER_2)

    def tearDown(self) -> None:
        """Clear db tables after each test"""
        with self.app_context:
            db.drop_all()

    def login(
        self, client: app.test_client, email: str, password: str
    ) -> LoginJSON:
        results = client.post(
            f"/members/login",
            data=json.dumps(
                {
                    "email": email,
                    "password": password,
                }
            ),
            headers={"Content-Type": "application/json"},
        )

        return json.loads(results.data)
