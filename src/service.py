# import falcon
import falcon.asgi
from Controller import OSEnv, UserAPI, AuthAPI

app = falcon.asgi.App()
authAPI = AuthAPI()
app.add_route("/auth/login", authAPI, suffix = 'login')
app.add_route("/auth/register", authAPI, suffix = 'register')
user_api = UserAPI()
app.add_route("/user", user_api)
app.add_route("/user/{id}", user_api)