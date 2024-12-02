import logging
from typing import List

import falcon
import pydantic_core
import sqlalchemy
from sqlalchemy.engine import Row
from sqlalchemy.orm import Query, joinedload
from falcon import Request, Response


from middleware import AuthRequired
from Service import SessionContext, PostModel, PostTagRelation
from APIModel import (
    JWTPayload,
    BasePostModel,
    UserViewDetailPostModel,
    UserViewListPostModel,
    UpdatePostModel,
    PostTagDTO,
)
from utils.role import UserRoleGroup


class PostAPI:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    @falcon.before(AuthRequired(UserRoleGroup.PUBLIC))
    async def on_get(self, req: Request, resp: Response):

        try:
            with SessionContext() as session:
                query = session.query(PostModel)
                posts: List[PostModel] = query.all()

                results = [
                    UserViewListPostModel.model_construct(**post.__dict__).model_dump()
                    for post in posts
                ]

        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.media = results

    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_post(self, req: Request, resp: Response):
        user: JWTPayload = req.context.user
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

    @falcon.before(AuthRequired(UserRoleGroup.PUBLIC))
    async def on_get_id(self, req: Request, resp: Response, post_id: int):
        user: JWTPayload = req.context.user
        try:
            with SessionContext() as session:
                query: Query = session.query(PostModel).where(PostModel.id == post_id)

                query = query.options(
                    joinedload(PostModel.tags), joinedload(PostModel.author)
                )

                postData: PostModel = query.first()

                if postData is None:
                    raise falcon.HTTPNotFound()

                isOwner = True if (user.user_id == postData.user_id) else False

                result = UserViewDetailPostModel.model_construct(**postData.__dict__)
                result.isOwner = isOwner
                respData = result.model_dump()
        except falcon.HTTPError as e:
            raise e
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.media = respData

    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_put_id(self, req: Request, resp: Response, post_id: int):
        user: JWTPayload = req.context.user
        try:
            reqData = await req.get_media()
            reqData = UpdatePostModel.model_validate(reqData)
            with SessionContext() as session:
                query: Query = session.query(PostModel).where(PostModel.id == id)

                postData: PostModel = query.first()

                if postData is None:
                    raise falcon.HTTPNotFound(description="post was not found.")

                if user.user_id != postData.user_id:
                    raise falcon.HTTPForbidden(
                        description="you are not the owner of post."
                    )

                updateData = reqData.model_dump()

                query.update(updateData)

        except falcon.HTTPError as e:
            raise e
        except pydantic_core.ValidationError as e:
            raise falcon.HTTPBadRequest(description=e.errors(include_url=False))
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_delete_id(self, req: Request, resp: Response, post_id: int):
        user: JWTPayload = req.context.user

        try:

            with SessionContext() as session:

                query: Query = session.query(PostModel).where(PostModel.id == id)
                userPost: PostModel = query.first()

                if userPost is None:
                    raise falcon.HTTPNotFound(description="post was not found.")

                if user.user_id != userPost.user_id:
                    raise falcon.HTTPForbidden(
                        description="you are not the owner of post."
                    )

                session.delete(userPost)

        except falcon.HTTPError as e:
            raise e
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))

        resp.status = falcon.HTTP_204

    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_post_tag(self, req: Request, resp: Response, post_id: int):
        user: JWTPayload = req.context.user

        try:
            reqData = await req.get_media()
            postAddDTO = PostTagDTO(post_id=post_id, tag_id=reqData["tag_id"])

            with SessionContext() as session:

                query: Query = session.query(PostModel.user_id).where(
                    PostModel.id == post_id
                )
                result: Row = query.first()

                if result["user_id"] != user.user_id:
                    raise falcon.HTTPForbidden(description="You are not the post owner")

                postTagRelation = PostTagRelation(**postAddDTO.model_dump())
                session.add(postTagRelation)

        except falcon.HTTPError as e:
            raise e
        except pydantic_core.ValidationError as e:
            raise falcon.HTTPBadRequest(
                description=e.errors(include_context=False, include_url=False)
            )
        except Exception as e:
            self.logger.debug(e)
            raise falcon.HTTPBadRequest()

    @falcon.before(AuthRequired(UserRoleGroup.ALL_USER))
    async def on_delete_tag(self, req: Request, resp: Response, post_id: int):
        user: JWTPayload = req.context.user
        try:
            reqData = await req.get_media()
            postTagDTO = PostTagDTO(post_id=post_id, tag_id=reqData["tag_id"])
            with SessionContext() as session:

                query: Query = session.query(PostModel.user_id).where(
                    PostModel.id == post_id
                )
                checkOwnerResult = query.first()

                if checkOwnerResult["user_id"] != user.user_id:
                    raise falcon.HTTPForbidden(description="You are not the post owner")

                query: Query = session.query(PostTagRelation).where(
                    sqlalchemy.and_(
                        PostTagRelation.post_id == post_id,
                        PostTagRelation.tag_id == postTagDTO.tag_id,
                    )
                )
                query.delete()

        except falcon.HTTPError as e:
            raise e
        except pydantic_core.ValidationError as e:
            raise falcon.HTTPBadRequest(
                description=e.errors(include_context=False, include_url=False)
            )
        except Exception as e:
            self.logger.debug(e)
            raise falcon.HTTPBadRequest()

        resp.status = falcon.HTTP_204
