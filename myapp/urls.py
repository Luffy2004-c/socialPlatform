from django.urls import path
from myapp.views import account, main, chat
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", account.register, name="register"),  # 用户注册
    path("login/", account.login, name="login-user"),  # 用户登录
    path("index/", main.index, name="index"),
    path("chat/<int:id>", chat.chat, name="chat-page"),
    path("chat/", chat.chat, name="chat-default-page"),
    path("logout/", account.logout, name="logout-user"),  # 用户注销登录
    path("friend/add/<int:id>", chat.add_friend, name="add-friend"),
    path("friend/list", chat.friends_list, name="friend-list"),
    path("friend/accept/<int:id>", chat.friend_accept, name="friend-accept"),
    path("message/send/<int:id>", chat.send_message, name="send-message"),
    path("setting/", account.setting, name="setting"),
    path("like/<int:id>", main.like, name="like"),
    path("comment/<int:dynamics_id>", main.send_commend, name="commend-send"),
    path("dynamics/release", main.dynamics_release, name="dynamic-release"),
]
