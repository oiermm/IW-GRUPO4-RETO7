from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class URLJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):

        header = self.get_header(request)

        if header is not None:
            raw_token = self.get_raw_token(header)

            if raw_token is not None:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token

        token = request.query_params.get('token')

        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
            return self.get_user(validated_token), validated_token

        except Exception:
            raise AuthenticationFailed(
                'El token es inválido o ha expirado.'
            )