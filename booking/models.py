from django.db import models
from django.utils.translation import gettext_lazy as _


class Booking(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=255,
    )
    email = models.EmailField(
        _("Email"),
    )
    time_slot = models.ForeignKey(
        "doctor.TimeSlot",
        null=False,
        on_delete=models.CASCADE,
    )
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)

    def __str__(self):
        return f"Booking for {self.email} @ {self.start_time}-{self.end_time}"
