from datetime import datetime
from typing import Dict, List

from flask_jwt_extended import decode_token, get_jwt, JWTManager
from functools import wraps

from custom_types import MemberJSON, TokenJSON
from models.member import MemberModel
from models.token import TokenModel

jwt = JWTManager()


class AuthError(Exception):
    """A standardized way to communicate auth failure modes"""

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class TokenNotFound(Exception):
    """
    Indicates that a token could not be found in the database
    """

    pass


@jwt.additional_claims_loader
def add_claims_to_jwt(identity: Dict) -> MemberJSON:
    return {
        "permissions": MemberModel.find_by_id(identity["id"]).get_permissions()
    }


# noinspection PyUnusedLocal
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(
    jwt_header: Dict[str, str], decoded_token: TokenJSON
) -> bool:
    jti = decoded_token["jti"]
    # noinspection PyBroadException
    try:
        token = TokenModel.query.filter_by(jti=jti).one()
        return token.revoked
    except Exception:
        return True


def add_token_to_database(tokens: List[str], member_id: int) -> None:
    for token in tokens:
        decoded_token = decode_token(token)
        jti = decoded_token["jti"]
        token_type = decoded_token["type"]
        expires = datetime.fromtimestamp(decoded_token["exp"])
        member_id = member_id

        TokenModel.revoke(member_id, token_type)

        token = TokenModel(
            jti=jti,
            token_type=token_type,
            expires=expires,
            revoked=False,
            member_id=member_id,
        )
        token.save_to_db()


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            permissions = get_jwt()["permissions"]

            if not permissions:
                raise AuthError(
                    {
                        "code": "invalid_permissions",
                        "description": "Permissions not included in JWT.",
                    },
                    400,
                )
            if permission not in permissions:
                raise AuthError(
                    {
                        "code": "unauthorized",
                        "description": "Permission not found.",
                    },
                    401,
                )
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
