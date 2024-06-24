from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from typing import Iterable, List, Optional, Union, Dict
from common.utils import parse_string

# class BaseModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    desc = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatar/", blank=True)
    gender = models.CharField(
        max_length=10, choices=(("male", "男"), ("female", "女")), default="male"
    )

    def __str__(self):
        return self.username

    def get_all_froups(self):
        return self.mygroups.all()

    def get_friends(self) -> List[Dict[str, Union[User, "PrivateMessage"]]] | None:
        friends = self.friends.all()
        # 获取用户和最近的历史记录
        friend_list = list(
            map(
                lambda x: {
                    "user": x.to_user,
                    "message": PrivateMessage.objects.filter(
                        (
                            models.Q(sender=self) & models.Q(recipient=x.to_user)
                            | (models.Q(sender=x.to_user) & models.Q(recipient=self))
                        )
                    ).first(),
                },
                friends,
            )
        )
        # 获取用户和最近的历史记录
        return friend_list

    def get_friendApplicationList(self) -> List[User] | None:
        return self.friend_requests_received.all()

    class Meta:
        verbose_name = "用户表"
        ordering = ["-created_at"]
        verbose_name_plural = verbose_name


class Friend(BaseModel, models.Model):  # TODO此处要在视图中添加一个好友双向创建的逻辑
    from_user = models.ForeignKey(
        User, related_name="friends", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="friend_requests_received", on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(default=False)  # 是否已经接受好友请求

    class Meta:
        verbose_name = "好友表"
        verbose_name_plural = verbose_name
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"


class Tag(BaseModel, models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "标签"
        ordering = ["-created_at"]
        verbose_name_plural = verbose_name


class Dynamics(BaseModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(
        "动态内容",
        max_length=1000,
    )
    PUBLIC_CHOICES = ((0, "Private"), (1, "Public"), (2, "OnlyFriends"))
    is_public = models.IntegerField("是否公开", choices=PUBLIC_CHOICES, default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name="dynamics")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    likes = models.ManyToManyField(User, related_name="like_dynamics", through="Like")

    def get_likes_count(self) -> int:
        """
        获取点赞数
        """
        return self.likes.count()

    def get_like_users(self) -> List[User]:
        """
        获取点赞用户列表
        """
        return self.likes.all()

    def save(self, *args, **kwargs):
        tags = self._extract_tags_from_content()
        super().save(*args, **kwargs)
        if tags:
            self.tags.add(*tags)

    def _extract_tags_from_content(self) -> List[Tag]:
        """
        保存未创建过的标签
        """
        tags = []
        words = self.content.split()
        words = parse_string(self.content)
        for word in words:
            tag, created = Tag.objects.get_or_create(name=word)
            tags.append(tag)
        return tags

    def get_all_comments(self):
        return self.comments.all().order_by("-created_at")

    def likes_action(self, user: User):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def __str__(self):
        return f"{self.user} - {self.content}"

    class Meta:
        verbose_name = "动态"
        ordering = ["-created_at"]
        verbose_name_plural = verbose_name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dynamics = models.ForeignKey(Dynamics, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "dynamics")  # 确保每个用户对每篇文章只能点赞一次

    def __str__(self):
        return f"{self.user.username} likes {self.dynamics}"


class Group(BaseModel, models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(default=" ", blank=True)
    users = models.ManyToManyField(User, through="GroupMemberShip")

    def __str__(self) -> str:
        return f"{self.name}"

    def get_members_with_roles(self):
        memberships = GroupMemberShip.objects.filter(group=self).select_related("user")
        members_with_roles = []
        for membership in memberships:
            members_with_roles.append(
                {
                    "user": membership.user,
                    "role": membership.get_role_display(),
                }
            )
        return members_with_roles

    def get_history_messages(self):
        return self.group_messages.all().order_by("-send_at")

    class Meta:
        verbose_name = "群组"
        ordering = ["-created_at"]
        verbose_name_plural = verbose_name


class GroupMemberShip(models.Model):
    MEMBER = "member"
    OWNER = "owner"

    ROLE_CHOICES = [
        (MEMBER, "Member"),
        (OWNER, "Owner"),
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_time = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)

    def __str__(self) -> str:
        return f"[group]{self.user} in {self.group}"

    class Meta:
        verbose_name = "群组成员表"
        verbose_name_plural = verbose_name
        unique_together = ("user", "group")


class PrivateMessage(models.Model):
    content = models.TextField(
        "消息内容",
        max_length=200,
    )
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )

    send_at = models.DateTimeField("发送时间", auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}:{self.content} at {self.send_at}"

    class Meta:
        verbose_name = "私信消息"
        ordering = ["-send_at"]
        verbose_name_plural = verbose_name


class GroupMessage(models.Model):
    content = models.TextField("群聊消息", max_length=200)
    sender = models.ForeignKey(
        User, related_name="sent_group_messages", on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group, related_name="group_messages", on_delete=models.CASCADE
    )
    send_at = models.DateTimeField("发送时间", auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in {self.group}:{self.content} at {self.send_at}"

    class Meta:
        verbose_name = "群聊消息"
        ordering = ["-send_at"]
        verbose_name_plural = verbose_name


class Comment(BaseModel, models.Model):
    content = models.TextField(
        "评论内容",
        max_length=200,
    )
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    dynamics = models.ForeignKey(
        Dynamics, related_name="comments", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    def __str__(self):
        return f"{self.user} commented on {self.dynamics}:{self.content}"

    def get_replies(self):
        return Comment.objects.filter(parent=self).order_by("-created_at")

    class Meta:
        verbose_name = "评论"
        ordering = ["-created_at"]
        verbose_name_plural = verbose_name


class Activity(BaseModel, models.Model):
    name = models.CharField("活动名称", max_length=100)
    description = models.TextField("活动描述", max_length=500)
    organizer = models.ForeignKey(
        User, related_name="organized_activities", on_delete=models.CASCADE
    )
    participants = models.ManyToManyField(
        User, through="Participant", related_name="activities_participated"
    )

    class Meta:
        verbose_name = "活动"
        ordering = ["-created_at"]
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "活动参与者"
        ordering = ["-joined_at"]
        unique_together = ("user", "activity")

    def __str__(self):
        return f"{self.user.username} - {self.activity.name}"


class ModelCreater:
    """
    用于指定群主，活动发起人等
    """

    def create_group(cls, group_name: str, group_owner: User):
        """
        创建群组，并指定群主为创建者
        """
        group = Group.objects.create(name=group_name)
        GroupMemberShip.objects.create(
            user=group_owner, group=group, role=GroupMemberShip.OWNER
        )

    def initiateActivities():
        """
        发起活动
        """
        activity = Activity.objects.create()
