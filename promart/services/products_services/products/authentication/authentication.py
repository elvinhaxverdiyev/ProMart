from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.authentication import get_authorization_header


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class that overrides the default JWT authentication mechanism.
    It retrieves the user from the token and adds it to the request object instead of querying the database.
    """

    def authenticate(self, request):
        """
        Authenticates the user by extracting and validating the JWT token from the request header.

        Args:
            request (HttpRequest): The incoming HTTP request containing the authorization header.

        Returns:
            tuple: A tuple containing the user object and the validated token if authentication is successful, 
                   or None if authentication is not possible.

        Raises:
            InvalidToken: If the token is invalid or does not contain a user_id.
        """
        # Retrieve the authorization header from the request
        header = self.get_header(request)
        if header is None:
            return None

        # Extract the raw token from the authorization header
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # Validate the token
        validated_token = self.get_validated_token(raw_token)

        # Extract user_id from the validated token
        user_id = validated_token.get("user_id")
        if not user_id:
            raise InvalidToken("Token does not contain user_id")

        # Instead of retrieving the user from the database, we return a simplified user object
        user = self.get_user_from_token(validated_token)

        return (user, validated_token)

    def get_user_from_token(self, validated_token):
        """
        Creates a simplified user object with the user_id from the validated token.

        Args:
            validated_token (dict): The validated JWT token containing user information.

        Returns:
            DummyUser: A dummy user object with the user_id and authentication status.
        """
        
        try:
            email = validated_token["email"]
            user_type = validated_token["user_type"]
        except KeyError:
            raise InvalidToken("Token is missing necessary user information")

        # Dummy user class to simulate a user object
        class DummyUser:
            def __init__(self, user_id, user_type, email):
                self.id = user_id
                self.email = email
                self.user_type = user_type
                self.is_authenticated = True

        return DummyUser(
            user_id=validated_token["user_id"],
            user_type=validated_token.get("user_type"),
            email=validated_token["email"]
        )
