from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from auth import requires_auth
from custom_types import ApiResponse
from models.role import RoleModel
from resources.message import (
    CREATED,
    DELETED,
    ERROR_404,
    ERROR_409,
    MODIFIED,
)
from schemas.role import RoleSchema

roles = Blueprint("roles", __name__)

role_schema = RoleSchema()
role_list_schema = RoleSchema(many=True)


@roles.route("/<int:role_id>")
@jwt_required()
@requires_auth("post:role")
def get_role(role_id: int) -> ApiResponse:
    role = RoleModel.find_by_id(role_id)

    if not role:
        abort(
            404,
            description=ERROR_404.format("Role", "id", role_id),
        )

    return (
        jsonify(
            {
                "role": role_schema.dump(role),
            }
        ),
        200,
    )


@roles.route("", methods=["POST"])
@jwt_required()
@requires_auth("post:role")
def post_role() -> ApiResponse:
    role_json = request.get_json()

    if RoleModel.find_by_name(role_json.get("role_name")):
        abort(
            409,
            description=ERROR_409.format(
                "Role",
                "role_name",
                role_json.get("role_name"),
            ),
        )

    role = role_schema.load(role_json)
    role.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("Role"),
                "role": role_schema.dump(role),
            }
        ),
        201,
    )


@roles.route("/<int:role_id>", methods=["PUT"])
@jwt_required()
@requires_auth("post:role")
def put_role(role_id: int) -> ApiResponse:
    role = RoleModel.find_by_id(role_id)

    if not role:
        abort(
            404,
            description=ERROR_404.format("Role", "id", role_id),
        )

    role_json = request.get_json()

    role_by_name = RoleModel.find_by_name(role_json.get("role_name"))

    if role_by_name and role_by_name.id != role_id:
        abort(
            409,
            description=ERROR_409.format(
                "Role",
                "role_name",
                role_json.get("role_name"),
            ),
        )

    role.role_name = role_json.get("role_name")
    role.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("Role"),
                "role": role_schema.dump(role),
            }
        ),
        200,
    )


@roles.route("/<int:role_id>", methods=["DELETE"])
@jwt_required()
@requires_auth("post:role")
def delete_role(role_id: int) -> ApiResponse:
    role = RoleModel.find_by_id(role_id)

    if not role:
        abort(
            404,
            description=ERROR_404.format("Role", "id", role_id),
        )

    role.delete_from_db()

    return (
        jsonify(
            {
                "message": DELETED.format("Role"),
                "role": role_schema.dump(role),
            }
        ),
        200,
    )


@roles.route("")
@jwt_required()
@requires_auth("post:role")
def get_roles() -> ApiResponse:
    role_list = RoleModel.find_all()

    return (
        jsonify({"roles": role_list_schema.dump(role_list)}),
        200,
    )
