from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import update_last_request


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        update_last_request(user)
        return user
