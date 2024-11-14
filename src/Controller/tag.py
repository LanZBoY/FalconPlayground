from typing import List

import falcon
from falcon import Request, Response

from sqlalchemy.orm import Query
# from sqlalchemy.engine import Row

from Service import SessionContext
from Service import TagModel
from APIModel import BaseTagDTO

class TagAPI:

    # TODO: 取得所有Tag or SearchTag
    async def on_get(self, req: Request, resp: Response):
        name = req.get_param("name")
        try:
            with SessionContext() as session:
                if (name is None):
                    query: Query = session.query(TagModel)
                else:
                    query: Query = session.query(TagModel).where(
                        TagModel.name.ilike(name)
                    )
                tags: List[TagModel] = query.all()

                respData = [BaseTagDTO.model_construct(**tag.__dict__).model_dump() for tag in tags]

                resp.media = respData

        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))
    
    # TODO: 建立Tag
    async def on_post(self, req: Request, resp: Response):
        reqData = await req.get_media()
        try:
            reqData = BaseTagDTO.model_validate(reqData)
            with SessionContext() as session:
                query: Query = session.query(TagModel).where(
                    TagModel.name == reqData.name
                )

                if (query.count() > 0):
                    raise falcon.HTTPBadRequest(description="Tag name has been exist.")

                insertData = TagModel(**reqData.model_dump())

                session.add(
                    insertData
                )

        except falcon.HTTPError as e:
            raise e
        except Exception as e:
            raise falcon.HTTPBadRequest(description=str(e))
    
    