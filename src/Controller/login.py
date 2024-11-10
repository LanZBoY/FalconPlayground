from falcon import Request, Response

import falcon

import jwt
from datetime import datetime, timedelta
import time
from utils.config import SECRET

class AuthAPI:

    async def on_post_login(self, req : Request, resp : Response):
        token = jwt.encode(payload={
            "iss": "WenTee",
            "exp":  (datetime.now() + timedelta(days=7)).timestamp()
        }, key=SECRET)
        resp.status = falcon.HTTP_501 


    async def on_post_register(self, req : Request, resp : Response):
        resp.status = falcon.HTTP_501 