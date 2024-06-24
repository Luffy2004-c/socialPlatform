from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from myapp.models import Dynamics, Comment, Friend, User, PrivateMessage
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def chat(request, id=None):
    user: User = request.tracer["user"]
    try:
        friend = User.objects.get(id=id)
    except Exception:
        friend = None
    context = {
        "active_menu": "chat",
        "user": user,
        "friend": friend,
        "friend_list": user.get_friends(),
    }
    if request.method == "GET":
        # 加载历史聊天记录
        condition_send = Q(
            sender_id=user.id,
            recipient_id=id,
        )
        condition_receive = Q(
            sender_id=id,
            recipient_id=user.id,
        )
        messages = PrivateMessage.objects.filter(
            condition_send | condition_receive
        ).order_by("send_at")
        context.update({"messages": messages})
        return render(request, "chat.html", context)


@csrf_exempt
def add_friend(request, id):
    user = request.tracer["user"]
    context = {
        "user": user.username,
        "status": True,
        "message": None,
        "is_friend": True,
        "button": None,
    }
    if request.method == "GET":
        to_friend_id = id
        if to_friend_id == user.id:
            context.update(settings.ADDFRIEND_MESSAGE["notself"])
            return JsonResponse(context)
        # 先查询当前用户是否与该id为friend关系
        condition1 = Q(
            from_user_id=user.id,
            to_user_id=to_friend_id,
        )
        condition2 = Q(
            from_user_id=to_friend_id,
            to_user_id=user.id,
        )
        condition3 = Q(is_accepted=True)
        if Friend.objects.filter(condition1 & Q(is_accepted=False)).exists():
            context.update(settings.ADDFRIEND_MESSAGE["havefor"])
            return JsonResponse(context)
        if Friend.objects.filter(
            (condition1 & condition3) | (condition2 & condition3)
        ).exists():
            context.update(settings.ADDFRIEND_MESSAGE["added"])
            print(context)
            return JsonResponse(context)
        else:
            context.update(settings.ADDFRIEND_MESSAGE["notAdded"])
            return JsonResponse(context)
    else:
        friend_id = id
        to_user = User.objects.get(id=friend_id)
        friend = Friend.objects.create(
            from_user=user, to_user=to_user, is_accepted=False
        )
        context.update({"message": f"已向{to_user.username}发送申请", "button": "添加"})
        return JsonResponse(context)


def friends_list(request):
    context = {"active_menu": "friend"}
    if request.method == "GET":
        user = request.tracer["user"]
        context.update({"user": user})
        friends = Friend.objects.filter(Q(from_user_id=user.id) | Q(to_user_id=user.id))
        context.update({"friends": friends})
        return render(request, "friend_list.html", context)


def friend_accept(request, id):
    user = request.tracer["user"]
    if request.method == "GET":
        try:
            friend_id = id
            friend = Friend.objects.get(id=friend_id)
            friend.is_accepted = True
            friend.save()
            return JsonResponse(
                {
                    "status": True,
                    "message": f"已接受{friend.from_user.username}的好友申请",
                    "type": "success",
                }
            )
        except Exception as e:
            return JsonResponse({"status": False, "message": e, "type": "error"})


@csrf_exempt
def send_message(request, id):
    user = request.tracer["user"]
    friend = User.objects.get(id=id)
    context = {
        "user": user.username,
        "status": True,
        "message": None,
    }
    if request.method == "POST":
        try:
            message = request.POST.get("content")
            print(message)
            message = PrivateMessage.objects.create(
                sender=user,
                recipient=friend,
                content=message,
            )
            context.update({"message": "发送成功"})
            return JsonResponse(context)
        except Exception as e:
            context.update({"status": False, "message": str(e)})
            return JsonResponse(context)
    else:
        return render(request, "chat.html", context)
