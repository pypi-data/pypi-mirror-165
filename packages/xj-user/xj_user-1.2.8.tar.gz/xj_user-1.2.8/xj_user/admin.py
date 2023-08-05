from django.contrib import admin
from config.config import Config
# 引入用户平台
from .models import *

config = Config()

# Register your models here.


class BaseInfoAdmin(admin.ModelAdmin):
    # fields = ('user_name', 'full_name', 'platform', 'platform_uid', 'phone', 'email', 'wechat', 'user_info')
    fields = ('user_name', 'full_name', 'nickname', 'phone', 'email', 'wechat_openid', 'user_info', 'user_group', 'permission', 'register_time')
    list_display = ('id', 'user_name', 'full_name', 'nickname', 'phone', 'email', 'wechat_openid', 'user_info', 'user_group', 'permission', 'register_time')
    search_fields = ('user_name', 'full_name', 'nickname', 'phone', 'user_group__group')
    list_filter = []


class AuthAdmin(admin.ModelAdmin):
    fields = ('user', 'password', 'token', 'ticket',)
    list_display = ('user', 'password', 'token', 'create_time', 'update_time',)
    search_fields = ('user', 'create_time')
    list_filter = ['user']

    # def platform(self, obj):
    #     return obj.platform


class DetailInfoAdmin(admin.ModelAdmin):
    fields = (
        'user', 'real_name', 'sex', 'birth', 'tags', 'signature', 'avatar', 'cover', 'language', 'region_code',
        'more',
        'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
        'field_10', 'field_11', 'field_12', 'field_13', 'field_14', 'field_15'
    )
    list_display = ('user', 'real_name', 'sex', 'birth', 'tags', 'avatar', 'cover', 'language', 'region_code')


class ExtendFiledAdmin(admin.ModelAdmin):
    fields = ('field', 'field_index', 'description')
    list_display = ('field', 'field_index', 'description')


class AccessLogAdmin(admin.ModelAdmin):
    fields = ('user', 'ip', 'create_time', 'client_info', 'more',)
    list_display = ('user', 'ip', 'create_time', 'client_info',)


class HistoryAdmin(admin.ModelAdmin):
    fields = ('user', 'field', 'old_value', 'new_value', 'create_time',)
    list_display = ('user', 'field', 'old_value', 'new_value', 'create_time',)


class RestrictRegionAdmin(admin.ModelAdmin):
    fields = ('user', 'region_code',)
    list_display = ('user', 'region_code',)


class PlatformAdmin(admin.ModelAdmin):
    fields = ('platform_id', 'platform_name')
    list_display = ('platform_id', 'platform_name')
    search_fields = ('platform_id', 'platform_name')


class PlatformsToUsersAdmin(admin.ModelAdmin):
    fields = ('platform', 'platform_user_id',)
    list_display = ('platform', 'platform_user_id',)


class PermissionAdmin(admin.ModelAdmin):
    fields = ('permission_id', 'permission_name',)
    list_display = ('permission_id', 'permission_name',)


class PermissionValueAdmin(admin.ModelAdmin):
    fields = ('permission', 'permission_value', 'type', 'is_system', 'is_ban',)
    list_display = ('permission', 'permission_value', 'type', 'is_system', 'is_ban',)


class GroupAdmin(admin.ModelAdmin):
    fields = ('group', 'parent_group', 'description')
    list_display = ('id', 'group', 'parent_group', 'description')


admin.site.register(BaseInfo, BaseInfoAdmin)
admin.site.register(Auth, AuthAdmin)
admin.site.register(DetailInfo, DetailInfoAdmin)
admin.site.register(AccessLog, AccessLogAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(RestrictRegion, RestrictRegionAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(PlatformsToUsers, PlatformsToUsersAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(PermissionValue, PermissionValueAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(ExtendFiled, ExtendFiledAdmin)
