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

    async def __call__(self, req: Request, resp: Response , resource, params : dict) -> Any:
        authorization : str = req.get_header(name="Authorization", default=None)
        userContent = None
        try:
            if(authorization is not None):
                _ , token = authorization.split(" ")
                content = jwt.decode(token, SECRET, algorithms=["HS256"])
                userContent = JWTPayload.model_validate(content['user'])
            else:
                userContent = JWTPayload(role=UserRole.GUEST)
                
        except jwt.InvalidSignatureError or jwt.InvalidTokenError as e:
            raise falcon.HTTPBadRequest(description="Token was invalided...")
        
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPBadRequest(description="Token was expired.")

        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))
        
        if(userContent.role not in self.role_required):
            raise falcon.HTTPForbidden()
        req.context.user = userContent