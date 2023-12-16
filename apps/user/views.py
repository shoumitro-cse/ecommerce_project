from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer, LogoutSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    This endpoint allows users to create a new account.

    Responses:
     - POST request:
        - 201 Created: Returns the newly registered user.
        - 400 Bad Request: If the request data is invalid.

    Example:
     ```http
     POST /api/register/
     ```
     Payload:
     ```json
     {
        "username": "new_user",
        "password": "secure_password",
        "email": "new_user@example.com"
        // Additional fields for the user
     }
     ```
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class UserLoginAPIView(APIView):
    """
    API endpoint for user login.

    This endpoint allows users to obtain access and refresh tokens for authentication.

    Responses:
     - POST request:
        - 200 OK: Returns the access and refresh tokens.
        - 400 Bad Request: If the request data is invalid.
        - 401 Unauthorized: If the credentials are invalid.

    Example:
       ```http
        POST /api/login/
       ```
      Payload:
      ```json
        {
            "username": "existing_user",
            "password": "existing_password"
        }
      ```
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'detail': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):
    """
    API endpoint for user logout.

    This endpoint allows users to blacklist their refresh token, logging them out.

    Responses:
     - POST request:
        - 200 OK: Returns a successful logout message.
        - 400 Bad Request: If the request data is invalid.
        - 401 Unauthorized: If the refresh token is invalid.

    Example:
      ```http
        POST /api/logout/
      ```
      Payload:
      ```json
        {
            "refresh_token": "valid_refresh_token"
        }
      ```
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = request.data.get('refresh_token')

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
                return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
            except TokenError:
                return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
