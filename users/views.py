

from django.http import HttpResponse
from django.shortcuts import render
import requests
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from knox.models import AuthToken
from knox.auth import TokenAuthentication

from .serializers import *
from django.views.decorators.csrf import csrf_exempt

from acount_book import settings

# Create your views here.

# 注册
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            user = serializer.save()
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 登录
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = AuthToken.objects.create(user)[1]
            return response.Response({"uid": user.id,
                                      "token": token}, 
                                     status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# 登出
class LogoutView(GenericAPIView):
    # authentication_classes = [knox.auth.TokenAuthentication, ] // knox.auth.TokenAuthentication
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        AuthToken.objects.filter(user = request.user).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

# 用户信息查询和修改
class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 只用于修改头像
    def post(self, request):
        user = request.user
        serializer = UserAvatarSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 微信登录, 自动注册
class WxLoginView(GenericAPIView):
    authentication_classes = [] # 不需要认证

    def post(self, request):
        code = request.data.get('code')
        if code is None:
            return response.Response({'msg': 'code不能为空'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 调用微信接口获取登录信息
        # https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
        url = settings.Code2Session_URL.format(settings.WX_APP_ID, settings.WX_APP_SECRET, code)
        r = requests.get(url)   # 返回JSON数据
        res = r.json()
        if 'errcode' in res:
            return response.Response({'msg': 'code无效'}, status=status.HTTP_400_BAD_REQUEST)


        # 根据openid查询用户
        user = MyUser.objects.filter(openid=res['openid']).first()
        if user is None:
            # 如果用户不存在，则创建用户
            user = MyUser.objects.create_user_with_openid(res['openid'])

        # 生成token
        token = AuthToken.objects.create(user)[1]
        return response.Response({'uid': user.id,
                                  'username': user.username,
                                  'token': token}, 
                                 status=status.HTTP_200_OK)
    