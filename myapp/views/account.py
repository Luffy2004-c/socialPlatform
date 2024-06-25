from typing import Any

from django.forms.forms import BaseForm
from myapp.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest, JsonResponse
from myapp.forms.user_form import RegisterModelForm, LoginModelForm, UserEditForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from common.encrypt import encrypt


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(
            request, "registration/register.html", {"form": form, "register": True}
        )
    else:
        form = RegisterModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            return HttpResponse(form.errors.as_json())


def login(request):
    if request.method == "GET":
        form = LoginModelForm()
        return render(request, "registration/login.html", {"form": form, "login": True})
    else:
        username = request.POST.get("username")
        password = encrypt(request.POST.get("password"))
        user = (
            User.objects.filter(Q(username=username) | Q(email=username))
            .filter(password=password)
            .first()
        )
        if user:
            request.session["user_id"] = user.id
            request.session.set_expiry(60 * 60 * 24 * 24)
            return redirect("/")
        else:
            return HttpResponse(form.errors.as_json())


def logout(request):  # 退出账号
    request.session.flush()
    return redirect("/login/")


def setting(request):
    user = request.tracer["user"]
    context = {"user": user, "active_menu": "setting"}
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/index")
        else:
            return HttpResponse(form.errors.as_json())
    else:
        form = UserEditForm(instance=user)
        context["form"] = form
        return render(request, "setting.html", context)
