from typing import List

import falcon
import pydantic_core
from sqlalchemy.orm import Query
from falcon import Request, Response


from middleware import AuthRequired
from Service import SessionContext, PostModel
from RequestModel import JWTPayload, BasePostModel, UserViewPostModel, UpdatePostModel
from utils.role import UserRoleGroup

class PostAPI:

    @falcon.before(AuthRequired(UserRoleGroup.PUBLIC))
    async def on_get(self, req : Request, resp : Response):

        try:
            with SessionContext() as session:
                query = session.query(PostModel)
                posts :List[PostModel]= query.all()
                
                results = [UserViewPostModel.model_validate(post).model_dump() for post in posts]


        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.media = results
    
    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_post(self, req: Request, resp: Response):
        user : JWTPayload = req.context.user
        try:
            postData = await req.get_media()
            postData = BasePostModel.model_validate(postData)

            with SessionContext() as session:
                postInDB = PostModel(**postData.model_dump())
                postInDB.user_id = user.user_id
                session.add(postInDB)

                postData = BasePostModel.model_construct(postInDB)

        except pydantic_core.ValidationError as e:
            raise falcon.HTTPBadRequest(description=e.errors(include_url=False))
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.status = falcon.HTTP_201
    
    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_put(self, req: Request, resp: Response, id: int):
        user : JWTPayload = req.context.user
        try:
            reqData = await req.get_media()
            reqData = UpdatePostModel.model_validate(reqData)
            with SessionContext() as session:
                query : Query = session.query(PostModel).where(
                    PostModel.id == id
                )

                postData : PostModel = query.first()

                if postData is None:
                    raise falcon.HTTPNotFound(description= "post was not found.")
                
                if user.user_id != postData.user_id:
                    raise falcon.HTTPForbidden(description= "you are not the owner of post.")
                
                updateData = reqData.model_dump()

                query.update(
                    updateData
                )

        except falcon.HTTPError as e:
            raise e
        except pydantic_core.ValidationError as e:
            raise falcon.HTTPBadRequest(description=e.errors(include_url=False))
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

    
    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_delete(self, req: Request, resp: Response, id :str):
        user : JWTPayload = req.context.user

        try:

            with SessionContext() as session:

                query : Query = session.query(PostModel).where(PostModel.id == id)
                userPost : PostModel = query.first()

                if userPost is None:
                    raise falcon.HTTPNotFound(description= "post was not found.")
                
                if user.user_id != userPost.user_id:
                    raise falcon.HTTPForbidden(description= "you are not the owner of post.")
                
                session.delete(userPost)

        except falcon.HTTPError as e:
            raise e
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.status = falcon.HTTP_204