from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Doctor(models.Model):
    CLINICAL = "clinical"
    ONLINE = "online"
    CONSULTATION_TYPE_CHOICES = (
        (
            CLINICAL,
            _("Clinical"),
        ),
        (
            ONLINE,
            _("Online"),
        ),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
    )
    consultation_type = models.CharField(
        _("Consultation Type"),
        max_length=50,
        default=ONLINE,
        choices=CONSULTATION_TYPE_CHOICES,
    )
    consultation_price = models.DecimalField(
        _("Consultation Price"),
        null=False,
        decimal_places=2,
        max_digits=10,
    )
    insurance_company = models.CharField(
        _("Insurance Company"),
        max_length=255,
        null=True,
        blank=True,
    )
    insurance_number = models.CharField(
        _("Insurance Number"),
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Doctor - {self.user}"


class Specialty(models.Model):
    # We need to add register this to model-translations but no need to add the package for just this field
    name = models.CharField(_("Name"), max_length=255, unique=True)
    doctors = models.ManyToManyField(
        Doctor,
        related_name="specialties",
    )

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    date = models.DateField(null=False)
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        null=False,
    )
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)

    class Meta:
        # We assume a doctor can set one time slot per day
        unique_together = ("doctor", "date")

    def __str__(self):
        return f"{self.doctor} available at {self.date}"

    @property
    def free_hours(self):
        """ return a list of (free_hour_start, free_hour_end) for the doctor at this date """
        bookings = self.booking_set.order_by("start_time")
        hours = []
        last_end_hour = self.start_time

        for booking in bookings:
            if booking.start_time > last_end_hour:
                end_hour = datetime.combine(self.date, booking.start_time) - timedelta(minutes=1)
                end_hour = end_hour.time()
                hours.append((last_end_hour, end_hour))
            last_end_hour = datetime.combine(self.date, booking.end_time) + timedelta(minutes=1)
            last_end_hour = last_end_hour.time()

        if self.end_time > last_end_hour:
            hours.append((last_end_hour, self.end_time))

        return hours

    def free_at(self, start_time, end_time):
        for start_free, end_free in self.free_hours:
            if start_time >= start_free and end_time <= end_free:
                return True
        return False
