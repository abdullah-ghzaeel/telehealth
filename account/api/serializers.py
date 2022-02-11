from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        required=True,
        allow_null=False,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        required=True,
        allow_null=False,
    )

    class Meta:
        # Used in custom validator
        required_fields = {
            "email": {
                "error_field_name": "email",
            },
            "password": {
                "error_field_name": "password",
            },
        }

    def validate(self, attrs):
        username = attrs.get("phone_number")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            msg = _("Unable to login with provided credentials")
            raise serializers.ValidationError(msg)

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            )
        ],
    )
    password_confirm = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        required=True,
        allow_null=False,
        write_only=True,
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "password",
            "password_confirm",
            "name",
            "email",
            "address",
        )

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        return user
