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