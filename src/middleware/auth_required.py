from typing import Any, Iterable
import falcon
import jwt
from falcon import Request, Response

from utils.role import UserRole
from utils.config import SECRET
from RequestModel import JWTPayload



class AuthRequired:

    def __init__(self, role_required : Iterable = [UserRole.ADMIN,]) -> None:
        self.role_required = set(role_required)


    async def __call__(self, req: Request, resp: Response , resource, params) -> Any:
        token : str = req.get_header(name="Authorization", default=None)
        _ , token = token.split(" ")
        try:
            content = jwt.decode(token, SECRET, algorithms=["HS256"])
            userContent = JWTPayload.model_validate(content['user'])

        except jwt.InvalidSignatureError or jwt.InvalidTokenError as e:
            raise falcon.HTTPBadRequest(description="Token was invalided...")
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))
        
        if(userContent.role not in self.role_required):
            raise falcon.HTTPForbidden()
        