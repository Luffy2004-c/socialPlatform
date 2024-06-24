from django.contrib import admin
from .models import *


class FriendshipInline(admin.TabularInline):
    model = Friend
    fk_name = "from_user"
    verbose_name = "好友"
    verbose_name_plural = "好友列表"


class DynamicsInline(admin.TabularInline):
    model = Dynamics
    verbose_name = "动态"
    verbose_name_plural = "动态列表"


class ActivityInline(admin.TabularInline):
    model = Activity
    verbose_name = "活动"
    verbose_name_plural = "活动列表"


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "get_friends_count")
    inlines = [FriendshipInline, DynamicsInline, ActivityInline]

    def get_friends_count(self, obj):
        return obj.friends.filter(is_accepted=True).count()

    get_friends_count.short_description = "好友数量"


class GroupMemberInline(admin.TabularInline):
    model = GroupMemberShip
    extra = 0
    verbose_name = "群组成员"
    verbose_name_plural = "群组成员"


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "desc",
        "get_members_count",
        "get_groupLeader",
    )  # 在群组列表中显示的字段
    inlines = [GroupMemberInline]  # 在群组详情页显示群组成员

    def get_members_count(self, obj):
        return obj.users.count()

    def get_groupLeader(self, obj):
        try:
            owner = GroupMemberShip.objects.filter(
                group=obj, role=GroupMemberShip.OWNER
            ).first()
            return owner.user.username
        except:
            return "暂无群主"

    get_members_count.short_description = "成员数量"  # 设置方法列的显示名称
    get_groupLeader.short_description = "群主"


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    verbose_name = "参与者"
    verbose_name_plural = "参与者"


class ActivatyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "organizer",
    )

    def get_paticipants_count(self, obj):
        return obj.participants.count()

    inlines = [ParticipantInline]


admin.site.register(User, UserAdmin)
admin.site.register(Dynamics)
admin.site.register(Comment)
admin.site.register(Friend)
admin.site.register(GroupMemberShip)
admin.site.register(Activity)
admin.site.register(Tag)
admin.site.register(PrivateMessage)

admin.register(Activity, ActivatyAdmin)
admin.register(Group)
# admin.register(Group, GroupAdmin)
