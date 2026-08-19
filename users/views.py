from django.views import generic

from users.serializers import UserSerializer


class UserRegistrationView(generic.CreateView):
    serializer_class = UserSerializer