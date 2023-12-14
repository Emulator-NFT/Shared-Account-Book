from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
# Register your models here.


class MyUserAdmin(UserAdmin):    
    list_display = ['id', 'username', 'openid']
    search_fields = ['username', 'openid']
    list_display_links = ['id', 'username']
    fieldsets = [
        ('基本信息', {'fields': ['openid', 'username', 'email', 'phone', 'avatar', 'date_joined']}),
        ('权限', {'fields': ['is_staff', 'is_active']})
    ]

# 上面两种MyUserAdmin都可以使用，但是ModelAdmin更像是一个普通的Model
# UserAdmin是一个专用于用户管理的Model，它定义了默认的创建用户的表单（比如密码二次确认）
admin.site.register(MyUser, MyUserAdmin)