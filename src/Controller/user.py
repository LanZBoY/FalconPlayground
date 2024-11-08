import falcon
import falcon.status_codes
from falcon import Request, Response
from Service import SessionContext, UserModel
from RequestModel import UserDTO

class UserApi:

    async def on_get(self, req : Request, resp : Response):
        with SessionContext() as session:
            try:
                q_result = session.query(UserModel.id, UserModel.username).all()
            except Exception as e:
                raise falcon.HTTPInternalServerError(title="ERROR", description=str(e))
            users = [UserDTO.model_validate(user).model_dump() for user in q_result]
            resp.media = users
        
    async def on_post(self, req: Request, resp: Response):
        reqData = await req.get_media()

        with SessionContext() as session:
            try:
                createUser = UserModel(**reqData)
                session.add(createUser)
            except Exception as e:
                raise falcon.HTTPBadRequest(title="Client Error", description=str(e))
        resp.status = falcon.status_codes.HTTP_201

    async def on_post_login(self, req: Request, resp: Response):
        reqData = await req.get_media()

        


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


    # async def on_delete(self, req: Request, resp: Response, id: int):
    #     with SessionContext() as session:
    #         try:
    #             res = session.query(UserModel).where(UserModel.id == id).first()
    #             session.delete(res)
    #         except Exception as e:
    #             raise falcon.HTTPBadRequest(title="Client Error", description=str(e))
            
    #         resp.status = falcon.HTTP_204
        
        

        
        
