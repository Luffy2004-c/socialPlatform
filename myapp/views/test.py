from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView


class MyLoginView(LoginView):
    form_class = len
    template_name = "your_app/login.html"

    def get_success_url(self):
        # 登录成功后的重定向URL
        return redirect("/your_success_url/")


def show_friends(request):
    user = request.user
    context = {}
    context.update(friends=user)
    return render(request, "index.html", {"s": 12})
