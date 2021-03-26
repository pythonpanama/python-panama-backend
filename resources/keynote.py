from flask import abort, Blueprint, jsonify, request

from custom_types import ApiResponse
from models.keynote import KeynoteModel
from resources.message import (
    CREATED,
    DELETED,
    ERROR_404,
    ERROR_404_LIST,
    MODIFIED,
)
from schemas.keynote import KeynoteSchema

keynotes = Blueprint("keynotes", __name__)

keynote_schema = KeynoteSchema()
keynote_list_schema = KeynoteSchema(many=True)


@keynotes.route("/<int:keynote_id>")
def get_keynote(keynote_id: int) -> ApiResponse:
    keynote = KeynoteModel.find_by_id(keynote_id)

    if not keynote:
        abort(404, description=ERROR_404.format("Keynote", "id", keynote_id))

    return (
        jsonify(
            {
                "keynote": keynote_schema.dump(keynote),
            }
        ),
        200,
    )


@keynotes.route("", methods=["POST"])
def post_keynote() -> ApiResponse:
    keynote_json = request.get_json()

    keynote = keynote_schema.load(keynote_json)
    keynote.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("Keynote"),
                "keynote": keynote_schema.dump(keynote),
            }
        ),
        201,
    )


@keynotes.route("/<int:keynote_id>", methods=["PUT"])
def put_keynote(keynote_id: int) -> ApiResponse:
    keynote = KeynoteModel.find_by_id(keynote_id)

    if not keynote:
        abort(404, description=ERROR_404.format("Keynote", "id", keynote_id))

    keynote_json = request.get_json()

    keynote.title = keynote_json.get("title")
    keynote.description = keynote_json.get("description")
    keynote.speaker_id = keynote_json.get("speaker_id")
    keynote.meeting_id = keynote_json.get("meeting_id")
    keynote.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("Keynote"),
                "keynote": keynote_schema.dump(keynote),
            }
        ),
        200,
    )


@keynotes.route("/<int:keynote_id>", methods=["DELETE"])
def delete_keynote(keynote_id: int) -> ApiResponse:
    keynote = KeynoteModel.find_by_id(keynote_id)

    if not keynote:
        abort(404, description=ERROR_404.format("Keynote", "id", keynote_id))

    keynote.delete_from_db()

    return (
        jsonify(
            {
                "message": DELETED.format("Keynote"),
                "keynote": keynote_schema.dump(keynote),
            }
        ),
        200,
    )


@keynotes.route("")
def get_keynotes() -> ApiResponse:
    keynote_list = KeynoteModel.find_all()

    if not keynote_list:
        abort(404, description=ERROR_404_LIST.format("keynotes"))

    return (
        jsonify({"keynotes": keynote_list_schema.dump(keynote_list)}),
        200,
    )


@keynotes.route("/meetings/<int:meeting_id>")
def get_keynotes_for_meeting(meeting_id: int) -> ApiResponse:
    keynote_list = KeynoteModel.find_by_meeting_id(meeting_id)

    if not keynote_list:
        abort(404, description=ERROR_404_LIST.format("keynotes"))

    return (
        jsonify({"keynotes": keynote_list_schema.dump(keynote_list)}),
        200,
    )


@keynotes.route("/speakers/<int:speaker_id>")
def get_keynotes_for_speaker(speaker_id: int) -> ApiResponse:
    keynote_list = KeynoteModel.find_by_speaker_id(speaker_id)

    if not keynote_list:
        abort(404, description=ERROR_404_LIST.format("keynotes"))

    return (
        jsonify({"keynotes": keynote_list_schema.dump(keynote_list)}),
        200,
    )
