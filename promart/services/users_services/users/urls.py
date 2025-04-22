from django.urls import path
from users.views import *

urlpatterns = [
    # User endpoints
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
        "users/<int:user_id>/type/",
        UserDetailView.as_view(),
        name="user-detail"
    ),

    # Password endpoints
    path(
        "change_password/",
        ChangePasswordView.as_view(),
        name="change-password"
    ),
    
    path(
        "reset_password",
        ResetPasswordView.as_view(),
        name="reset-password"
    ),
    
    path(
        "send_code_reset_password",
        ResetPasswordSendCodeView.as_view(),
        name="send-code-reset-password"
    ),

]