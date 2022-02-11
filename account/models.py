from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber
from sms import send_sms


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not phone_number:
            raise ValueError("The given phone_number must be set")
        validate_international_phonenumber(phone_number)
        user = self.model(
            phone_number=phone_number,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        u = self.create_user(phone_number, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(
        _("Phone number"),
        unique=True,
    )
    email = models.EmailField(
        _("Email address"),
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        null=True,
        blank=True,
    )
    address = models.TextField(
        _("Address"),
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.phone_number} - {self.name}"


class PhoneVerification(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="rel_phone_verify"
    )
    code = models.CharField(max_length=8)

    def __str__(self):
        return self.code

    @staticmethod
    def get_random_number():
        return get_random_string(length=4, allowed_chars="1234567890")

    @classmethod
    def generate_code(cls, user):
        """
        generate verification code for given user
        """

        obj, is_updated = cls.objects.update_or_create(
            user=user, defaults={"code": cls.get_random_number()}
        )
        return obj

    def dispatch(self):
        send_sms(
            f"Your code is {self.code}",
            "+12065550100",
            [str(self.user.phone_number)],
            fail_silently=False,
        )
