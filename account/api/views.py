from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserLoginSerializer


class LoginView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("phone_number")
        password = serializer.data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(_("Invalid phone or password"))

        if not user.is_active:
            raise ValidationError(_("Please confirm your phone number"))

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "id": user.id,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
