from flask import abort, Blueprint, jsonify, request

from custom_types import ApiResponse
from models.speaker import SpeakerModel
from resources.message import (
    CREATED,
    DELETED,
    ERROR_404,
    ERROR_404_LIST,
    ERROR_409,
    MODIFIED,
)
from schemas.speaker import SpeakerSchema

speakers = Blueprint("speakers", __name__)

speaker_schema = SpeakerSchema()
speaker_list_schema = SpeakerSchema(many=True)


@speakers.route("/<int:speaker_id>")
def get_speaker(speaker_id: int) -> ApiResponse:
    speaker = SpeakerModel.find_by_id(speaker_id)

    if not speaker:
        abort(
            404,
            description=ERROR_404.format("Speaker", "id", speaker_id),
        )

    return (
        jsonify(
            {
                "speaker": speaker_schema.dump(speaker),
            }
        ),
        200,
    )


@speakers.route("", methods=["POST"])
def post_speaker() -> ApiResponse:
    speaker_json = request.get_json()

    speaker = speaker_schema.load(speaker_json)
    speaker.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("Speaker"),
                "speaker": speaker_schema.dump(speaker),
            }
        ),
        201,
    )


@speakers.route("/<int:speaker_id>", methods=["PUT"])
def put_speaker(speaker_id: int) -> ApiResponse:
    speaker = SpeakerModel.find_by_id(speaker_id)

    if not speaker:
        abort(
            404,
            description=ERROR_404.format("Speaker", "id", speaker_id),
        )

    speaker_json = request.get_json()
    speaker.first_name = speaker_json.get("first_name")
    speaker.last_name = speaker_json.get("last_name")
    speaker.email = speaker_json.get("email")
    speaker.linkedin_profile = speaker_json.get("linkedin_profile")
    speaker.github_profile = speaker_json.get("github_profile")
    speaker.twitter_profile = speaker_json.get("twitter_profile")
    speaker.bio = speaker_json.get("bio")
    speaker.profile_picture = speaker_json.get("profile_picture")
    speaker.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("Speaker"),
                "speaker": speaker_schema.dump(speaker),
            }
        ),
        200,
    )


@speakers.route("/<int:speaker_id>", methods=["DELETE"])
def delete_speaker(speaker_id: int) -> ApiResponse:
    speaker = SpeakerModel.find_by_id(speaker_id)

    if not speaker:
        abort(
            404,
            description=ERROR_404.format("Speaker", "id", speaker_id),
        )

    speaker.delete_from_db()

    return (
        jsonify(
            {
                "message": DELETED.format("Speaker"),
                "speaker": speaker_schema.dump(speaker),
            }
        ),
        200,
    )


@speakers.route("")
def get_speakers() -> ApiResponse:
    speaker_list = SpeakerModel.find_all()

    if not speaker_list:
        abort(404, description=ERROR_404_LIST.format("speakers"))

    return (
        jsonify({"speakers": speaker_list_schema.dump(speaker_list)}),
        200,
    )
