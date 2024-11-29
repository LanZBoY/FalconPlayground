# import falcon
import falcon.asgi
from Controller import (UserAPI,
                        AuthAPI,
                        SuperUserAPI,
                        PostAPI, 
                        TagAPI)
from Controller import (
    SSEAPI, BroadcastAPI
)
import logging
from utils.config import DEBUG_MODE

if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG)

app = falcon.asgi.App()

superuserAPI = SuperUserAPI()
app.add_route("/superuser", superuserAPI)

authAPI = AuthAPI()
app.add_route("/auth/login", authAPI, suffix = 'login')
app.add_route("/auth/register", authAPI, suffix = 'register')

userAPI = UserAPI()
app.add_route("/user", userAPI)
app.add_route("/user/me", userAPI, suffix = "me")
app.add_route("/user/{id:int}", userAPI)

postAPI = PostAPI()
app.add_route("/post", postAPI)
app.add_route("/post/{post_id:int}", postAPI, suffix = "id")
app.add_route("/post/{post_id:int}/tag", postAPI, suffix = "tag")


tagAPI = TagAPI()
app.add_route("/tag", tagAPI)

broadcastApi = BroadcastAPI()
app.add_route("/broadcast", broadcastApi)

sseApi = SSEAPI()
app.add_route("/sse", sseApi)