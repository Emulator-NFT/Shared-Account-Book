import uuid
from acount_book.settings import CONTAINER_BASE_URL, REMOTE_BASE_URL
from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import MyUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    

# 不能继承ModelSerializer，因为会自动调用create方法，而登录不需要创建用户
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user is not None:
            return user
        else:
            raise serializers.ValidationError('用户名或密码错误')
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'openid', 'username', 'nickname', 'avatar', 'date_joined']
        extra_kwargs = {
            'openid': {'read_only': True},
            'username': {'read_only': True},
            'avatar': {'read_only': True}, # 不能在此修改头像，只能通过专门的接口修改
            'date_joined': {'read_only': True},
        }
    # 默认情况下，DRF已经返回avatar的完整URL
    avatar = serializers.SerializerMethodField()
    def get_avatar(self, obj):
        base_url = self.context['request'].build_absolute_uri('/')[:-1]
        base_url = base_url.replace(CONTAINER_BASE_URL, REMOTE_BASE_URL)
        # http://127.0.0.1:8000 + /media/avatars/house_Sxphalw.jpg
        if obj.avatar:
            return base_url + obj.avatar.url
        else:
            return None

# 用户头像
class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'write_only': True}
        }