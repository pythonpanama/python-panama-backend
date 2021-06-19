import json
from typing import Tuple
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
    TEST_KEYNOTE_1,
    TEST_KEYNOTE_2,
    TEST_MEMBER_1,
    TEST_MEMBER_2,
    TEST_MEETING_1,
    TEST_MEETING_2,
    TEST_PERMISSION_1,
    TEST_PERMISSION_2,
    TEST_PERMISSION_3,
    TEST_PERMISSION_4,
    TEST_PERMISSION_5,
    TEST_PERMISSION_6,
    TEST_PERMISSION_7,
    TEST_PERMISSION_8,
    TEST_PROJECT_1,
    TEST_PROJECT_2,
    TEST_ROLE_1,
    TEST_ROLE_2,
    TEST_ROLE_3,
    TEST_ROLE_4,
    TEST_ROLE_5,
    TEST_SPEAKER_1,
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

            self.keynote_1 = KeynoteModel(**TEST_KEYNOTE_1)
            self.keynote_2 = KeynoteModel(**TEST_KEYNOTE_2)
            self.member_1 = MemberModel(**TEST_MEMBER_1)
            self.member_2 = MemberModel(**TEST_MEMBER_2)
            self.meeting_1 = MeetingModel(**TEST_MEETING_1)
            self.meeting_2 = MeetingModel(**TEST_MEETING_2)
            self.permission_1 = PermissionModel(**TEST_PERMISSION_1)
            self.permission_2 = PermissionModel(**TEST_PERMISSION_2)
            self.permission_3 = PermissionModel(**TEST_PERMISSION_3)
            self.permission_4 = PermissionModel(**TEST_PERMISSION_4)
            self.permission_5 = PermissionModel(**TEST_PERMISSION_5)
            self.permission_6 = PermissionModel(**TEST_PERMISSION_6)
            self.permission_7 = PermissionModel(**TEST_PERMISSION_7)
            self.permission_8 = PermissionModel(**TEST_PERMISSION_8)
            self.project_1 = ProjectModel(**TEST_PROJECT_1)
            self.project_2 = ProjectModel(**TEST_PROJECT_2)
            self.role_1 = RoleModel(**TEST_ROLE_1)
            self.role_2 = RoleModel(**TEST_ROLE_2)
            self.role_3 = RoleModel(**TEST_ROLE_3)
            self.role_4 = RoleModel(**TEST_ROLE_4)
            self.role_5 = RoleModel(**TEST_ROLE_5)
            self.speaker_1 = SpeakerModel(**TEST_SPEAKER_1)
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

    def add_permissions_to_admin(self):
        role_1 = self.role_1.save_to_db()
        permission_1 = self.permission_1.save_to_db()
        permission_2 = self.permission_2.save_to_db()
        permission_3 = self.permission_3.save_to_db()
        permission_4 = self.permission_4.save_to_db()
        permission_5 = self.permission_5.save_to_db()
        permission_6 = self.permission_6.save_to_db()
        permission_7 = self.permission_7.save_to_db()
        permission_8 = self.permission_8.save_to_db()
        role_1.permissions.append(permission_1)
        role_1.permissions.append(permission_2)
        role_1.permissions.append(permission_3)
        role_1.permissions.append(permission_4)
        role_1.permissions.append(permission_5)
        role_1.permissions.append(permission_6)
        role_1.permissions.append(permission_7)
        role_1.permissions.append(permission_8)

        return role_1

    def add_keynote_to_db(
        self,
        keynote: KeynoteModel,
        role: RoleModel,
        member: MemberModel,
        speaker: SpeakerModel,
        meeting: MeetingModel,
    ) -> Tuple[
        KeynoteModel, MemberModel, RoleModel, SpeakerModel, MeetingModel
    ]:
        speaker = self.add_speaker_to_db(speaker)
        meeting, member, role = self.add_meeting_to_db(meeting, member, role)
        keynote = keynote.save_to_db()
        return keynote, member, role, speaker, meeting

    def add_meeting_to_db(
        self, meeting: MeetingModel, member: MemberModel, role: RoleModel
    ) -> Tuple[MeetingModel, MemberModel, RoleModel]:
        member, role = self.add_member_to_db(member, role)
        meeting = meeting.save_to_db()
        return meeting, member, role

    def add_member_to_db(
        self, member: MemberModel, role: RoleModel
    ) -> Tuple[MemberModel, RoleModel]:
        role = self.add_role_to_db(role)
        member = member.save_to_db()
        return member, role

    def add_permission_to_db(
        self, permission: PermissionModel
    ) -> PermissionModel:
        return permission.save_to_db()

    def add_role_to_db(self, role: RoleModel) -> RoleModel:
        return role.save_to_db()

    def add_speaker_to_db(self, speaker: SpeakerModel) -> SpeakerModel:
        return speaker.save_to_db()
