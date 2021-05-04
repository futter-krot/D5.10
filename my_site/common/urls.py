from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.views import login, logout

app_name = "common"

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
