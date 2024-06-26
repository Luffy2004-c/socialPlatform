from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from myapp.models import Dynamics, Comment, User, Like
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import Http404
from myapp.forms.dynamics__form import DynamicsModelForm


def index(request):
    user: User = request.tracer["user"]
    context: dict = {
        "user": user,
        "active_menu": "dynamic",
        "recent_messages": user.get_recent_messages(),
        "dynamics": None,
        "is_active": None,
        "dynamics_click": None,
        "comments": None,
        "package": None,
    }
    if request.method == "GET":
        dynamics = Dynamics.objects.filter(
            Q(is_public=1)
        ).all()  # TODO如果有时间，后面改成只显示公开和只对好友可见的动态
        comments = Comment.objects.filter().all()[:5]

        context["dynamics"] = dynamics
        context["comments"] = comments
        dynamics_id = request.GET.get("dynamics_id", None)
        if dynamics_id:
            obj = Dynamics.objects.filter(id=dynamics_id).first()
            context.update(
                dynamics_click=obj,
                is_active="is-active",
                package=obj.InformationPackaging(),
                is_like_user=obj.is_like_user(user),
            )

        return render(request, "index.html", context)


def like(request, id):
    user = request.tracer["user"]
    if request.method == "GET":
        dynamics = Dynamics.objects.filter(id=id).first()
        is_liked = request.GET.get("is_liked", None)
        like_count = dynamics.get_likes_count()
        if is_liked == "Y":
            try:
                get_object_or_404(Like, **{"user": user, "dynamics": dynamics})
                Like.objects.filter(user=user, dynamics=dynamics).delete()
                like_count -= 1
            except Http404:
                pass
        else:
            Like.objects.create(user=user, dynamics=dynamics)
            like_count += 1
        return JsonResponse(
            {
                "status": True,
                "like_count": like_count,
                "is_liked": "Y" if is_liked == "N" else "Y",
            }
        )


@csrf_exempt
def send_commend(request, dynamics_id):
    user = request.tracer["user"]
    data = {"user": user, "dynamics_id": dynamics_id}
    if request.method == "POST":
        type = request.POST.get("type", None)
        content = request.POST.get("content", None)
        if type == "reply":
            data.update(parent_id=request.POST.get("parent_id", None))
        Comment.objects.create(**data, content=content)
        return JsonResponse({"status": True})


@csrf_exempt
def dynamics_release(request):
    user = request.tracer["user"]
    if request.method == "GET":
        form = DynamicsModelForm()
        return render(request, "dynamics_release.html", {"form": form})
    else:
        form = DynamicsModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect("index")
