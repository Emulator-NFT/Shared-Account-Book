

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView

from knox.models import AuthToken
from knox.auth import TokenAuthentication

from .serializers import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = AuthToken.objects.create(user)[1]
            return response.Response({"uid": user.id,
                                      "avatar": user.avatar,
                                      "token": token}, 
                                     status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(GenericAPIView):
    # authentication_classes = [knox.auth.TokenAuthentication, ] // knox.auth.TokenAuthentication
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        AuthToken.objects.filter(user = request.user).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)