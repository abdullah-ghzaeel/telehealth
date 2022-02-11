from django.urls import path, include

urlpatterns = [
    path(
        "account/",
        include(
            "account.api.urls",
            namespace="account_api",
        ),
    ),
    path(
        "doctor/",
        include(
            "doctor.api.urls",
            namespace="doctor_api",
        ),
    ),
    path(
        "booking/",
        include(
            "booking.api.urls",
            namespace="booking_api",
        ),
    ),
]
