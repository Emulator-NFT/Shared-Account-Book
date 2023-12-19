import uuid
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

# 用户头像
class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['avatar']
        extra_kwargs = {
            'avatar': {'write_only': True}
        }