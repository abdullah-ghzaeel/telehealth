from django.utils.translation import gettext as _
from rest_framework import serializers

from booking.models import Booking
from doctor.models import TimeSlot


class BookingSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, instance):
        return instance.time_slot.date

    def validate(self, attrs):
        time_slot = attrs["time_slot"]
        if not time_slot.free_at(attrs["start_time"], attrs["end_time"]):
            raise serializers.ValidationError(_("Invalid time"))
        return attrs

    class Meta:
        model = Booking
        fields = (
            "id",
            "name",
            "email",
            "date",
            "start_time",
            "end_time",
            "time_slot",
        )
        read_only_fields = ("id",)
