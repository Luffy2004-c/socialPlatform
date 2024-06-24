from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from myapp.models import Dynamics, Comment
from django.db.models import Q


def index(request):
    context: dict = {"user": request.tracer["user"], "active_menu": "dynamic"}
    if request.method == "GET":
        dynamics = Dynamics.objects.filter(
            Q(is_public=1)
        ).all()  # TODO如果有时间，后面改成只显示公开和只对好友可见的动态
        comments = Comment.objects.filter().all()[:5]

        context["dynamics"] = dynamics
        context["comments"] = comments
        return render(request, "index.html", context)