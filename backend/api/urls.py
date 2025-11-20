from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.CreateUserView.as_view(), name="register"),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='refresh'),
]

