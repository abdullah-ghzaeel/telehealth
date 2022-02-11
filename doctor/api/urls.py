from django.urls import path, include
from .views import (
    DoctorSignUpView,
    DoctorVerifyView,
    DoctorProfileView,
    TimeSlotView,
    DoctorBookingView,
)

app_name = "doctor_api"


urlpatterns = [
    path(
        "sign-up/",
        include(
            [
                path(
                    "",
                    DoctorSignUpView.as_view(),
                    name="sign_up",
                ),
                path(
                    "verify/",
                    DoctorVerifyView.as_view(),
                    name="verify",
                ),
            ]
        ),
    ),
    path(
        "account",
        DoctorProfileView.as_view(),
        name="account",
    ),
    path(
        "time-slot",
        TimeSlotView.as_view(),
        name="time_slot",
    ),
    path(
        "bookings",
        DoctorBookingView.as_view(),
        name="bookings",
    ),
]
