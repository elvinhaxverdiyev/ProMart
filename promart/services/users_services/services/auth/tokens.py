from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["user_type"] = user.user_type
    refresh["email"] = user.email 
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }  