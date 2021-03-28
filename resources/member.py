from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash

from auth import add_token_to_database
from custom_types import ApiResponse
from models.member import MemberModel
from models.token import TokenModel
from resources.message import (
    ACTIVATED,
    CREATED,
    DEACTIVATED,
    EMAIL_MODIFIED,
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
        refresh_token = create_refresh_token(identity)
        add_token_to_database([access_token, refresh_token], member.id)

        return (
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
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
