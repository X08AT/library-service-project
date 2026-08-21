from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers import UserSerializer


@extend_schema(
    summary="User registration",
    description="Create a new user.",
    request=UserSerializer,
    responses=UserSerializer,
)
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserManageView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        summary="Retrieve User",
        description="Retrieve user data.",
        responses=UserSerializer,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update User",
        description="Update user data.",
        request=UserSerializer,
        responses=UserSerializer,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Partial Update User",
        description="Partially update user data.",
        request=UserSerializer,
        responses=UserSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@extend_schema(
    summary="Obtain JWT Token",
    description="Obtain an access and refresh JWT token pair using user credentials.",
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    summary="Refresh JWT Token",
    description="Obtain a new access token using a valid refresh token.",
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
