from django.urls import path


from users.views import (
    UserRegistrationView,
    UserManageView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

app_name = "users"

urlpatterns = [
    path("users/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "users/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("users/", UserRegistrationView.as_view(), name="create"),
    path("users/me/", UserManageView.as_view(), name="manage"),
]
