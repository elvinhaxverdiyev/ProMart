from django.urls import path
from users.views import *

urlpatterns = [
    path(
        "register/", 
        RegisterView.as_view(),
        name="register"
    ),
    
    path(
        "send_verification_code",
        SendVerificationCodeView.as_view(),
        name="send-verification-code"
    ),
]