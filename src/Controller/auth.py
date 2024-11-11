from falcon import Request, Response

import falcon
import jwt
import hashlib
from uuid import uuid4
from datetime import datetime, timedelta
from pydantic_core import ValidationError
from sqlalchemy.orm import Query

from Service import SessionContext, UserModel
from RequestModel import UserRegisterDTO, UserLoginDTO, JWTPayload
from utils.config import SECRET

class AuthAPI:

    async def on_post_login(self, req : Request, resp : Response):
        reqData = await req.get_media()

        try:
            reqData = UserLoginDTO.model_validate(reqData)
            reqData.password = hashlib.sha256(reqData.password.encode()).hexdigest()
            with SessionContext() as session:
                query : Query = session.query(UserModel).where(
                    UserModel.username == reqData.username,
                    UserModel.password == reqData.password
                )

                result : UserModel = query.first()
                if(result is None):
                    raise falcon.HTTPNotFound()
                
                
                
                exposeInfo = JWTPayload.model_validate(result)
                

        except Exception as e:
            raise e
        
        try:

            token = jwt.encode(payload={
                "iss": "JimLiu",
                "exp":  (datetime.now() + timedelta(days=7)).timestamp(),
                "user": exposeInfo.model_dump()
            }, key=SECRET)

        except Exception as e:
            print(e)
            raise e
        
        resp.status = falcon.HTTP_200 
        resp.media = {
            "token" : token
        }


    async def on_post_register(self, req : Request, resp : Response):
        reqData = await req.get_media()
        
        try:
            reqData = UserRegisterDTO.model_validate(reqData)
            reqData.password = hashlib.sha256(reqData.password.encode()).hexdigest()
            with SessionContext() as session:

                result : Query = session.query(UserModel.username).filter_by(username = reqData.username)

                if(result.count() > 0):
                    raise falcon.HTTPBadRequest(description="username has been existed.")

                userModel = UserModel(**reqData.model_dump())
                userModel.role = "NORMAL"
                session.add(userModel)


        except ValidationError as e:
            raise falcon.HTTPBadRequest(description=e.errors())
        except falcon.HTTPBadRequest as e:
            raise e
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))
        resp.status = falcon.HTTP_200