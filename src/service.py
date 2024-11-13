# import falcon
import falcon.asgi
from Controller import OSEnv, UserAPI, AuthAPI, SuperUserAPI, PostAPI, TagAPI

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
app.add_route("/post/{id:int}", postAPI, suffix = "id")

tagAPI = TagAPI()
app.add_route("/tag", tagAPI)
# app.add_route("/tag", tagAPI, suffix="byName")