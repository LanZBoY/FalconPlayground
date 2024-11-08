# import falcon
import falcon.asgi
from Controller import OSEnv, UserApi

app = falcon.asgi.App()
app.add_route("/env", OSEnv())
user_api = UserApi()
app.add_route("/user", user_api)
app.add_route("/user/{id}", user_api)