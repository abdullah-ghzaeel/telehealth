from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.api.serializers import UserSerializer
from account.models import PhoneVerification
from doctor.models import Doctor, Specialty, TimeSlot

User = get_user_model()


class SpecialtySerializer(serializers.ModelSerializer):
    # we need to remove unique validator
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
    )

    class Meta:
        model = Specialty
        fields = ("id", "name")
        read_only_fields = ("id",)


class DoctorSignUpSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        required=True,
        allow_null=False,
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            )
        ],
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        required=True,
        allow_null=False,
        write_only=True,
    )
    password_confirm = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        required=True,
        allow_null=False,
        write_only=True,
    )
    name = serializers.CharField(
        required=True,
        allow_null=False,
        write_only=True,
    )
    email = serializers.EmailField(
        required=True,
        allow_null=False,
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            )
        ],
    )
    address = serializers.CharField(
        required=True,
        allow_null=False,
        write_only=True,
    )
    specialties = SpecialtySerializer(many=True)
    user = UserSerializer(read_only=True)

    def validate(self, attrs):
        user_serializer = UserSerializer(data=attrs)
        user_serializer.is_valid(raise_exception=True)
        return attrs

    class Meta:
        model = Doctor
        fields = (
            "id",
            "phone_number",
            "password",
            "password_confirm",
            "name",
            "email",
            "address",
            "consultation_type",
            "consultation_price",
            "insurance_company",
            "insurance_number",
            "user",
            "specialties",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        user_data = {
            "phone_number": validated_data.pop("phone_number"),
            "password": validated_data.pop("password"),
            "password_confirm": validated_data.pop("password_confirm"),
            "name": validated_data.pop("name"),
            "email": validated_data.pop("email"),
            "address": validated_data.pop("address"),
        }
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid()
        user = user_serializer.save()
        user.is_active = False
        user.save()
        validated_data["user"] = user
        phone_code = PhoneVerification.generate_code(user)
        phone_code.dispatch()

        specialties = validated_data.pop("specialties")

        instance = super(DoctorSignUpSerializer, self).create(validated_data)

        for specialty_data in specialties:
            specialty, creaated = Specialty.objects.get_or_create(
                name=specialty_data["name"]
            )
            specialty.doctors.add(instance)
            specialty.save()

        return instance


class DoctorVerifySerializer(serializers.Serializer):
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.filter(
            user__is_active=False,
        ),
        write_only=True,
    )
    code = serializers.CharField(
        write_only=True,
    )
    message = serializers.SerializerMethodField()

    def get_message(self, instance):
        return _("Your account was activated")

    def validate(self, attrs):
        phone_code_qs = PhoneVerification.objects.filter(
            code=attrs.pop("code"),
            user=attrs["doctor"].user,
        )
        if not phone_code_qs.exists():
            raise serializers.ValidationError(_("code is invalid"))
        phone_code_qs.delete()
        return attrs

    def create(self, validated_data):
        doctor = validated_data.pop("doctor")
        user = doctor.user
        user.is_active = True
        user.save()
        return doctor


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specialties = SpecialtySerializer(
        many=True,
    )

    class Meta:
        model = Doctor
        fields = (
            "id",
            "consultation_type",
            "consultation_price",
            "insurance_company",
            "insurance_number",
            "user",
            "specialties",
        )
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        specialties = validated_data.pop("specialties")

        instance = super(DoctorProfileSerializer, self).update(instance, validated_data)

        instance.specialties.clear()
        for specialty_data in specialties:
            specialty, created = Specialty.objects.get_or_create(
                name=specialty_data["name"]
            )
            specialty.doctors.add(instance)
            specialty.save()

        return instance


class TimeSlotSerializer(serializers.ModelSerializer):
    def validate_date(self, date):
        doctor = self.context["request"].user.doctor
        if TimeSlot.objects.filter(date=date, doctor=doctor).exists():
            raise serializers.ValidationError(_("Time Slot Is Already Set"))
        return date

    def validate(self, attrs):
        attrs["doctor"] = self.context["request"].user.doctor
        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError(_("Please select a valid range"))
        return attrs

    class Meta:
        model = TimeSlot
        fields = (
            "id",
            "date",
            "start_time",
            "end_time",
        )
        read_only_fields = ("id",)
