from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from auth import requires_auth
from custom_types import ApiResponse
from models.permission import PermissionModel
from resources.message import (
    CREATED,
    DELETED,
    ERROR_404,
    ERROR_409,
    MODIFIED,
)
from schemas.permission import PermissionSchema

permissions = Blueprint("permissions", __name__)

permission_schema = PermissionSchema()
permission_list_schema = PermissionSchema(many=True)


@permissions.route("/<int:permission_id>")
@jwt_required()
@requires_auth("post:permission")
def get_permission(permission_id: int) -> ApiResponse:
    permission = PermissionModel.find_by_id(permission_id)

    if not permission:
        abort(
            404,
            description=ERROR_404.format("Permission", "id", permission_id),
        )

    return (
        jsonify(
            {
                "permission": permission_schema.dump(permission),
            }
        ),
        200,
    )


@permissions.route("", methods=["POST"])
@jwt_required()
@requires_auth("post:permission")
def post_permission() -> ApiResponse:
    permission_json = request.get_json()

    if PermissionModel.find_by_name(permission_json.get("permission_name")):
        abort(
            409,
            description=ERROR_409.format(
                "Permission",
                "permission_name",
                permission_json.get("permission_name"),
            ),
        )

    permission = permission_schema.load(permission_json)
    permission.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("Permission"),
                "permission": permission_schema.dump(permission),
            }
        ),
        201,
    )


@permissions.route("/<int:permission_id>", methods=["PUT"])
@jwt_required()
@requires_auth("post:permission")
def put_permission(permission_id: int) -> ApiResponse:
    permission = PermissionModel.find_by_id(permission_id)

    if not permission:
        abort(
            404,
            description=ERROR_404.format("Permission", "id", permission_id),
        )

    permission_json = request.get_json()

    permission_by_name = PermissionModel.find_by_name(
        permission_json.get("permission_name")
    )

    if permission_by_name and permission_by_name.id != permission_id:
        abort(
            409,
            description=ERROR_409.format(
                "Permission",
                "permission_name",
                permission_json.get("permission_name"),
            ),
        )

    permission.permission_name = permission_json.get("permission_name")
    permission.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("Permission"),
                "permission": permission_schema.dump(permission),
            }
        ),
        200,
    )


@permissions.route("/<int:permission_id>", methods=["DELETE"])
@jwt_required()
@requires_auth("post:permission")
def delete_permission(permission_id: int) -> ApiResponse:
    permission = PermissionModel.find_by_id(permission_id)

    if not permission:
        abort(
            404,
            description=ERROR_404.format("Permission", "id", permission_id),
        )

    permission.delete_from_db()

    return (
        jsonify(
            {
                "message": DELETED.format("Permission"),
                "permission": permission_schema.dump(permission),
            }
        ),
        200,
    )


@permissions.route("")
@jwt_required()
@requires_auth("post:permission")
def get_permissions() -> ApiResponse:
    permission_list = PermissionModel.find_all()

    return (
        jsonify({"permissions": permission_list_schema.dump(permission_list)}),
        200,
    )
