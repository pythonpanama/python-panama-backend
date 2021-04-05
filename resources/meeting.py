from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from auth import requires_auth
from custom_types import ApiResponse
from models.meeting import MeetingModel
from resources.message import (
    CREATED,
    DELETED,
    ERROR_404,
    ERROR_404_LIST,
    MODIFIED,
)
from schemas.meeting import MeetingSchema

meetings = Blueprint("meetings", __name__)

meeting_schema = MeetingSchema()
meeting_list_schema = MeetingSchema(many=True)


@meetings.route("/<int:meeting_id>")
@jwt_required()
@requires_auth("get:member")
def get_meeting(meeting_id: int) -> ApiResponse:
    meeting = MeetingModel.find_by_id(meeting_id)

    if not meeting:
        abort(404, description=ERROR_404.format("Meeting", "id", meeting_id))

    return (
        jsonify(
            {
                "meeting": meeting_schema.dump(meeting),
            }
        ),
        200,
    )


@meetings.route("", methods=["POST"])
@jwt_required()
@requires_auth("post:meeting")
def post_meeting() -> ApiResponse:
    meeting_json = request.get_json()

    meeting = meeting_schema.load(meeting_json)
    meeting.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("Meeting"),
                "meeting": meeting_schema.dump(meeting),
            }
        ),
        201,
    )


@meetings.route("/<int:meeting_id>", methods=["PUT"])
@jwt_required()
@requires_auth("post:meeting")
def put_meeting(meeting_id: int) -> ApiResponse:
    meeting = MeetingModel.find_by_id(meeting_id)

    if not meeting:
        abort(404, description=ERROR_404.format("Meeting", "id", meeting_id))

    meeting_json = request.get_json()

    meeting.datetime = meeting_json.get("datetime")
    meeting.type = meeting_json.get("type")
    meeting.location = meeting_json.get("location")
    meeting.description = meeting_json.get("description")
    meeting.creator_id = meeting_json.get("creator_id")
    meeting.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("Meeting"),
                "meeting": meeting_schema.dump(meeting),
            }
        ),
        200,
    )


@meetings.route("/<int:meeting_id>", methods=["DELETE"])
@jwt_required()
@requires_auth("post:meeting")
def delete_meeting(meeting_id: int) -> ApiResponse:
    meeting = MeetingModel.find_by_id(meeting_id)

    if not meeting:
        abort(404, description=ERROR_404.format("Meeting", "id", meeting_id))

    meeting.delete_from_db()

    return (
        jsonify(
            {
                "message": DELETED.format("Meeting"),
                "meeting": meeting_schema.dump(meeting),
            }
        ),
        200,
    )


@meetings.route("")
@jwt_required()
@requires_auth("post:keynote")
def get_meetings() -> ApiResponse:
    meeting_list = MeetingModel.find_all()

    if not meeting_list:
        abort(404, description=ERROR_404_LIST.format("meetings"))

    return (
        jsonify({"meetings": meeting_list_schema.dump(meeting_list)}),
        200,
    )
