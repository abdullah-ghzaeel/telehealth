from django.urls import path, include
from .views import BookDoctorView

app_name = "booking_api"

urlpatterns = [
    path(
        "book",
        BookDoctorView.as_view(),
        name="book",
    ),
]
