from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
# Register your models here.


# 继承 UserAdmin 比较麻烦，看官方文档示例还需要自定义表单
# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email']
#     search_fields = ['username', 'email']
#     fieldsets = [
#         ('基本信息', {'fields': ['username', 'email', 'phone', 'avatar']}),
#         ('权限', {'fields': ['is_staff', 'is_active']})
#     ]

# 必须显示定义fieldsets，因为继承了 UserAdmin，
# 默认的 fieldsets 有 last_name date_joined 但是MyUser没有
class MyUserAdmin(UserAdmin):    
    list_display = ['username', 'email']
    fieldsets = [
        ('基本信息', {'fields': ['username', 'email', 'phone', 'avatar', 'date_joined']}),
        ('权限', {'fields': ['is_staff', 'is_active']})
    ]

# 上面两种MyUserAdmin都可以使用，但是ModelAdmin更像是一个普通的Model
# UserAdmin是一个专用于用户管理的Model，它定义了默认的创建用户的表单（比如密码二次确认）
admin.site.register(MyUser, MyUserAdmin)