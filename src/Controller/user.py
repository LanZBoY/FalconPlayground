import falcon
import falcon.status_codes
from falcon import Request, Response

from sqlalchemy.orm import Query

from Service import SessionContext, UserModel
from middleware import AuthRequired
from utils.role import UserRole
from RequestModel import UserListView

class UserAPI:

    # Only Admin can get All user...
    @falcon.before(AuthRequired(role_required=(UserRole.ADMIN,)))
    async def on_get(self, req : Request, resp : Response):

        with SessionContext() as session:
            try:
                query : Query = session.query(UserModel.id, UserModel.username, UserModel.email, UserModel.address)
                user_list = query.all()
            except Exception as e:
                raise falcon.HTTPInternalServerError(title="ERROR", description=str(e))
            users = [UserListView.model_validate(user).model_dump() for user in user_list]
            resp.media = users


    @falcon.before(AuthRequired(role_required=(UserRole.ADMIN,)))
    async def on_delete(self, req: Request, resp: Response, id: int):

        if(id is None):
            raise falcon.HTTPBadRequest()

        with SessionContext() as session:
            try:
                res : UserModel = session.query(UserModel).where(UserModel.id == id).first()

                if(res == None):
                    resp.status = falcon.HTTP_NO_CONTENT
                    return

                if(res.role == UserRole.ADMIN):
                    raise falcon.HTTPForbidden(description="")
                
                session.delete(res)
            except falcon.HTTPError as e:
                raise e
            except Exception as e:
                raise falcon.HTTPBadRequest(description=str(e))
            
            resp.status = falcon.HTTP_204

    # async def on_post(self, req: Request, resp: Response):
    #     resp.status = falcon.HTTP_501
    #     reqData = await req.get_media()

    #     with SessionContext() as session:
    #         try:
    #             createUser = UserModel(**reqData)
    #             session.add(createUser)
    #         except Exception as e:
    #             raise falcon.HTTPBadRequest(title="Client Error", description=str(e))
    #     resp.status = falcon.status_codes.HTTP_201

        


    # TODO:Only Admin can delete data.
    # TODO:Only user owner can modify data. 

    # async def on_put(self, req: Request, resp: Response, id : int):
    #     reqData : dict = await req.get_media()
    #     with SessionContext() as session:
    #         try:
    #             res = session.query(UserModel).where(UserModel.id == id).update(
    #                 reqData
    #             )
    #         except Exception as e:
    #             raise falcon.HTTPBadRequest(title="Client Error", description=str(e))



        
        

        
        
