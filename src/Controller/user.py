import falcon
import falcon.status_codes
from falcon import Request, Response
from Service import SessionContext
from Service import UserModel
from RequestModel import UserDTO

class UserApi:

    async def on_get(self, req : Request, resp : Response):
        with SessionContext() as session:
            try:
                q_result = session.query(UserModel).all()
            except Exception as e:
                raise falcon.HTTPInternalServerError(title="ERROR", description=str(e))
            users = [UserDTO.model_validate(user).model_dump() for user in q_result]
            resp.media = users
        
    async def on_post(self, req: Request, resp: Response):
        reqData = await req.get_media()
        createUser = UserModel(**reqData)

        with SessionContext() as session:
            try:
                session.add(createUser)
            except Exception as e:
                raise falcon.HTTPBadRequest(title="Client Error", description=str(e))
        
        resp.status = falcon.status_codes.HTTP_201

        
        

        
        
