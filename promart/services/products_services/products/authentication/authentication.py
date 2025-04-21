from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.authentication import get_authorization_header


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        # İstifadəçini bazadan tapmaq əvəzinə sadəcə request-ə əlavə edirik
        user_id = validated_token.get("user_id")
        if not user_id:
            raise InvalidToken("Token does not contain user_id")

        # request.user və ya request.auth istəyəndə lazım olacaq
        user = self.get_user_from_token(validated_token)

        return (user, validated_token)

    def get_user_from_token(self, validated_token):
        # user obyektini yaratmadan sadə object kimi qaytarırıq
        class DummyUser:
            def __init__(self, user_id):
                self.id = user_id
                self.is_authenticated = True

        return DummyUser(validated_token["user_id"])
