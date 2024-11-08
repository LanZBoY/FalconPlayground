import falcon
from falcon import Response, Request

from utils import config
class OSEnv:

    async def on_get(self, req: Request, resp: Response):
        resp.content_type = falcon.MEDIA_TEXT
        resp.text = config.ENVIRONMENT