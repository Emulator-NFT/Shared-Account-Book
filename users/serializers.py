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
        fields = ['username', 'email', 'phone', 'avatar']
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True}
        }
    
    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        # instance.avatar = validated_data.get('avatar', instance.avatar)
        new_avatar = validated_data.get('avatar', None)
        if new_avatar is not None:
            instance.avatar.delete(save=False)
            file_extension = new_avatar.name.split('.')[-1]
            new_avatar.name = str(uuid.uuid4()) + '.' + file_extension
            instance.avatar = new_avatar
        instance.save()
        return instance