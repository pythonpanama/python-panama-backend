from flask import abort, Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from auth import requires_auth
from custom_types import ApiResponse
from models.project import ProjectModel
from resources.message import (
    CREATED,
    DELETED,
    ERROR_404,
    ERROR_404_LIST,
    ERROR_409,
    MODIFIED,
)
from schemas.project import ProjectSchema

projects = Blueprint("projects", __name__)

project_schema = ProjectSchema()
project_list_schema = ProjectSchema(many=True)


@projects.route("/<int:project_id>")
def get_project(project_id: int) -> ApiResponse:
    project = ProjectModel.find_by_id(project_id)

    if not project:
        abort(
            404,
            description=ERROR_404.format("Project", "id", project_id),
        )

    return (
        jsonify(
            {
                "project": project_schema.dump(project),
            }
        ),
        200,
    )


@projects.route("", methods=["POST"])
def post_project() -> ApiResponse:
    project_json = request.get_json()

    if ProjectModel.find_by_title(project_json.get("title")):
        abort(
            409,
            description=ERROR_409.format(
                "Project",
                "title",
                project_json.get("title"),
            ),
        )

    project = project_schema.load(project_json)
    project.save_to_db()

    return (
        jsonify(
            {
                "message": CREATED.format("project"),
                "project": project_schema.dump(project),
            }
        ),
        201,
    )


@projects.route("/<int:project_id>", methods=["PUT"])
def put_project(project_id: int) -> ApiResponse:
    project = ProjectModel.find_by_id(project_id)

    if not project:
        abort(
            404,
            description=ERROR_404.format("Project", "id", project_id),
        )

    project_json = request.get_json()

    project_by_title = ProjectModel.find_by_title(project_json.get("title"))

    if project_by_title and project_by_title.id != project_id:
        abort(
            409,
            description=ERROR_409.format(
                "Project",
                "title",
                project_json.get("title"),
            ),
        )

    project.start_date = project_json.get("start_date")
    project.end_date = project_json.get("end_date")
    project.title = project_json.get("title")
    project.description = project_json.get("description")
    project.goals = project_json.get("goals")
    project.status = project_json.get("status")
    project.admin_id = project_json.get("admin_id")
    project.save_to_db()

    return (
        jsonify(
            {
                "message": MODIFIED.format("project"),
                "project": project_schema.dump(project),
            }
        ),
        200,
    )


@projects.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id: int) -> ApiResponse:
    project = ProjectModel.find_by_id(project_id)

    if not project:
        abort(
            404,
            description=ERROR_404.format("Project", "id", project_id),
        )

    project.delete_from_db()

    return (
        jsonify(
            {
                "message": DELETED.format("project"),
                "project": project_schema.dump(project),
            }
        ),
        200,
    )


@projects.route("")
def get_projects() -> ApiResponse:
    project_list = ProjectModel.find_all()

    if not project_list:
        abort(404, description=ERROR_404_LIST.format("projects"))

    return (
        jsonify({"projects": project_list_schema.dump(project_list)}),
        200,
    )
