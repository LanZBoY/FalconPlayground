import falcon
from falcon import Request, Response


class TagAPI:

    async def on_get(self, req: Request, reps: Response):
        raise falcon.HTTPNotImplemented()