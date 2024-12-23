import falcon
import pydantic_core
import hashlib
import falcon.status_codes
from falcon import Request, Response
from sqlalchemy.orm import Query
from sqlalchemy.engine import Row

from Service import SessionContext, UserModel
from middleware import AuthRequired
from utils.role import UserRoleGroup, UserRole
from utils.config import CREATE_SECRET
from APIModel import (
    OwnerView_User,
    AdminView_User,
    UserUpdateDTO,
    JWTPayload,
    UserRegisterDTO,
)


async def requireSecret(req: Request, resp: Response, resource, param: dict):
    reqData = await req.get_media()

    if ("SECRET" not in reqData) or reqData["SECRET"] != CREATE_SECRET:
        resp.status = falcon.HTTP_404
        return


@falcon.before(requireSecret)
class SuperUserAPI:

    async def on_post(self, req: Request, resp: Response):
        reqData = await req.get_media()

        try:
            superadmin = UserRegisterDTO.model_validate(reqData)
            superadmin.password = hashlib.sha256(
                superadmin.password.encode()
            ).hexdigest()
            superadmin = superadmin.model_dump()
            superadmin["role"] = UserRole.ADMIN

            with SessionContext() as session:
                userModel = UserModel(**superadmin)
                session.add(userModel)

        except pydantic_core.ValidationError as e:
            raise falcon.HTTPBadRequest(description=e.errors())


class UserAPI:

    @falcon.before(AuthRequired(role_required=UserRoleGroup.ALL_USER))
    async def on_get_me(self, req: Request, resp: Response):
        user: JWTPayload = req.context.user

        with SessionContext() as session:
            try:
                query: Query = session.query(
                    UserModel.username, UserModel.email, UserModel.address
                ).where(UserModel.id == user.user_id)
                userData: Row = query.first()
                if userData is None:
                    raise falcon.HTTPNotFound()
                res = OwnerView_User.model_construct(**userData).model_dump()
            except falcon.HTTPError() as e:
                raise e
            except Exception as e:
                raise falcon.HTTPBadRequest(description=str(e))

            resp.media = res

    @falcon.before(AuthRequired(role_required=UserRoleGroup.ALL_USER))
    async def on_put_me(self, req: Request, resp: Response):
        user: JWTPayload = req.context.user

        reqData = await req.get_media()
        reqData = UserUpdateDTO.model_validate(reqData).model_dump()
        try:
            with SessionContext() as session:
                query: Query = session.query(UserModel).where(
                    UserModel.id == user.user_id
                )
                query.update(reqData)
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

    # Only Admin can get All user...
    @falcon.before(AuthRequired(role_required=UserRoleGroup.ONLY_ADMIN))
    async def on_get(self, req: Request, resp: Response):

        try:
            with SessionContext() as session:
                query: Query = session.query(
                    UserModel.id, UserModel.username, UserModel.email, UserModel.address
                )
                user_list: Row = query.all()
        except Exception as e:
            raise falcon.HTTPInternalServerError(title="ERROR", description=str(e))

        users = [
            AdminView_User.model_construct(**user).model_dump() for user in user_list
        ]
        resp.media = users

    @falcon.before(AuthRequired(role_required=UserRoleGroup.ONLY_ADMIN))
    async def on_delete(self, req: Request, resp: Response, id: int):
        user: JWTPayload = req.context.user
        if id is None:
            raise falcon.HTTPBadRequest()
        try:
            with SessionContext() as session:
                res: UserModel = (
                    session.query(UserModel).where(UserModel.id == id).first()
                )

                if res == None:
                    resp.status = falcon.HTTP_NO_CONTENT
                    return

                if user.role != UserRole.ADMIN:
                    raise falcon.HTTPForbidden(description="")

                session.delete(res)
        except falcon.HTTPError as e:
            raise e
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.status = falcon.HTTP_204
