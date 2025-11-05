from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class CreateUserView (generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] #PERMITE ACCEDER A CUALQUIERA INCLUSO SI NO ESTA AUTENTICADO, ES DECIR, CUALQUIERA PUEDE CREAR UN NUEVO USUARIO 


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer