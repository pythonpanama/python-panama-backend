from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash

from auth import add_token_to_database, requires_auth
from custom_types import ApiResponse
from models.member import MemberModel
from models.token import TokenModel
from resources.message import (
    ACTIVATED,
    CREATED,
    DEACTIVATED,
    ERROR_401,
    ERROR_404,
    ERROR_409,
    MEMBER_401,
    MODIFIED,
    PASSWORD_MODIFIED,
)
from schemas.member import MemberSchema

members = Blueprint("members", __name__)

member_schema = MemberSchema()
member_list_schema = MemberSchema(many=True)


@members.route("/login", methods=["POST"])
def login() -> ApiResponse:
    """Login a member"""
    member_json = request.get_json()
    email = member_json["email"]
    password = member_json["password"]

    member = MemberModel.find_by_email(email)

    if member and member.verify_password(password) and member.is_active:
        identity = member_schema.dump(member)
        access_token = create_access_token(identity=identity, fresh=True)
        _refresh_token = create_refresh_token(identity=identity)
        add_token_to_database([access_token, _refresh_token], member.id)

        return (
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": _refresh_token,
                    "member": identity,
                },
            ),
            200,
        )

    abort(401, description=MEMBER_401)


@members.route("/logout")
@jwt_required()
def logout() -> ApiResponse:
    """Logout a member"""
    member = get_jwt_identity()
    result = TokenModel.revoke(member["id"])

    return jsonify({"message": result["message"]}), result["status"]


@members.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    add_token_to_database([access_token], identity["id"])

    return (
        jsonify(
            {
                "access_token": access_token,
                "member": identity,
            },
        ),
        200,
    )


@members.route("/<int:member_id>")
@jwt_required()
@requires_auth("get:member")
def get_member(member_id: int) -> ApiResponse:
    member = MemberModel.find_by_id(member_id)

    if not member:
        abort(404, description=ERROR_404.format("Member", "id", member_id))

    return (
        jsonify(
            {
                "member": member_schema.dump(member),
            }
        ),
        200,
    )


@members.route("", methods=["POST"])
def post_member() -> ApiResponse:
    member_json = request.get_json()

    if MemberModel.find_by_email(member_json.get("email")):
        abort(
            409,
            description=ERROR_409.format(
                "Member",
                "email",
                member_json.get("email"),
            ),
        )

    member = member_schema.load(member_json)
    member.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("Member"),
                "member": member_schema.dump(member),
            }
        ),
        201,
    )


@members.route("/<int:member_id>", methods=["PUT"])
@jwt_required(fresh=True)
@requires_auth("get:member")
def put_member(member_id: int) -> ApiResponse:
    member = MemberModel.find_by_id(member_id)
    identity = get_jwt_identity()

    if member and identity["id"] != member.id:
        abort(
            401,
            description=ERROR_401,
        )

    if not member:
        abort(
            404,
            description=ERROR_404.format("Member", "id", member_id),
        )

    member_json = request.get_json()

    member_by_email = MemberModel.find_by_email(member_json.get("email"))

    if member_by_email and member_by_email.id != member_id:
        abort(
            409,
            description=ERROR_409.format(
                "Member",
                "email",
                member_json.get("email"),
            ),
        )

    member.email = member_json.get("email")
    member.mobile_phone = member_json.get("mobile_phone")
    member.first_name = member_json.get("first_name")
    member.last_name = member_json.get("last_name")
    member.linkedin_profile = member_json.get("linkedin_profile")
    member.github_profile = member_json.get("github_profile")
    member.twitter_profile = member_json.get("twitter_profile")
    member.profile_picture = member_json.get("profile_picture")
    member.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("Member"),
                "member": member_schema.dump(member),
            }
        ),
        200,
    )


@members.route("/<int:member_id>/activate", methods=["PUT"])
@jwt_required(fresh=True)
@requires_auth("activate:member")
def activate_member(member_id: int) -> ApiResponse:
    member = MemberModel.find_by_id(member_id)

    if not member:
        abort(404, description=ERROR_404.format("Member", "id", member_id))

    member.is_active = True
    member.save_to_db()

    return (
        jsonify(
            {
                "message": ACTIVATED.format("Member"),
                "member": member_schema.dump(member),
            }
        ),
        200,
    )


@members.route("/<int:member_id>/deactivate", methods=["PUT"])
@jwt_required(fresh=True)
@requires_auth("activate:member")
def deactivate_member(member_id: int) -> ApiResponse:
    member = MemberModel.find_by_id(member_id)

    if not member:
        abort(404, description=ERROR_404.format("Member", "id", member_id))

    member.is_active = False
    member.save_to_db()

    return (
        jsonify(
            {
                "message": DEACTIVATED.format("Member"),
                "member": member_schema.dump(member),
            }
        ),
        200,
    )


@members.route("/<int:member_id>/change_password", methods=["PUT"])
@jwt_required(fresh=True)
@requires_auth("get:member")
def change_member_password(member_id: int) -> ApiResponse:
    member = MemberModel.find_by_id(member_id)
    identity = get_jwt_identity()

    if member and identity["id"] != member.id:
        abort(
            401,
            description=ERROR_401,
        )

    if not member:
        abort(404, description=ERROR_404.format("Member", "id", member_id))

    member_json = request.get_json()
    member.password_hash = generate_password_hash(member_json.get("password"))
    member.save_to_db()

    return (
        jsonify(
            {
                "message": PASSWORD_MODIFIED,
                "member": member_schema.dump(member),
            }
        ),
        200,
    )
