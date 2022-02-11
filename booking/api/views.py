from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from .serializers import BookingSerializer


class BookDoctorView(
    CreateAPIView
):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
