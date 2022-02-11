from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsDoctor
from doctor.models import TimeSlot
from booking.models import Booking
from booking.api.serializers import BookingSerializer

from doctor.api.serializers import (
    DoctorSignUpSerializer,
    DoctorVerifySerializer,
    DoctorProfileSerializer,
    TimeSlotSerializer,
)


class DoctorSignUpView(CreateAPIView):
    serializer_class = DoctorSignUpSerializer
    permission_classes = [AllowAny]


class DoctorVerifyView(CreateAPIView):
    serializer_class = DoctorVerifySerializer
    permission_classes = [AllowAny]


class DoctorProfileView(mixins.UpdateModelMixin, RetrieveAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_object(self):
        return self.request.user.doctor

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DoctorQuerySetMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(doctor=self.request.user.doctor)
        return qs


class TimeSlotView(
    DoctorQuerySetMixin,
    mixins.CreateModelMixin,
    ListAPIView
):
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    queryset = TimeSlot.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DoctorBookingView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsDoctor]
    queryset = Booking.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(time_slot__doctor=self.request.user.doctor)
        return qs
