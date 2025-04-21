from django.urls import path
from users.views import *

urlpatterns = [
    path(
        "register/", 
        RegisterView.as_view(),
        name="register"
    ),
    
    path(
        "send_verification_code/",
        SendVerificationCodeView.as_view(),
        name="send-verification-code"
    ),
    
    path(
        "login/",
        LoginView.as_view(), 
        name="login"
    ),
    
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),
    
    path(
        "users/",
        UserListView.as_view(),
        name="user-list"
    ),
    
    path(
        "users/<int:user_id>/type",
        UserDetailView.as_view(),
        name="user-detail"
    ),

]