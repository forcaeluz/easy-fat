from django.db import models
from django.core.validators import ValidationError
from datetime import timedelta

from flocks.models import Flock


# Create your models here.
class Medicine(models.Model):
    name = models.TextField(unique=True, null=False)
    recommended_age_start = models.IntegerField()
    recommended_age_stop = models.IntegerField()
    dosage_per_kg = models.FloatField()
    grace_period_days = models.IntegerField()
    instructions = models.TextField()

    def clean(self):
        if self.recommended_age_start >= self.recommended_age_stop:
            raise ValidationError('Start age should be smaller than stop age.', code='Start age bigger than stop age')

        super(models.Model, self).clean()

    @property
    def availability(self):
        """
            Property that tells how much of this medicine is available at the farm.
        :return: A float value, indicating how much. The units depend on the units used for this medicine.
        :rtype: float
        """
        return 0

    @property
    def is_recommended_for_flock(self, flock):
        """
            This property tells if this medicine is recommended to give to a certain flock.
        :rtype: bool
        :param flock: The flock for which the condition is being checked.
        :return: True if it is recommended, false otherwise.
        """
        assert isinstance(flock, Flock)
        # Include logic to determine is medicine should be
        # suggested to this flock or not.
        return True


class Treatment(models.Model):
    start_date = models.DateField()
    stop_date = models.DateField(null=True)
    medicine = models.ForeignKey(Medicine)
    flock = models.ForeignKey(Flock)
    comments = models.TextField()

    @property
    def is_active(self):
        return self.stop_date is None

    @property
    def end_date_grace_period(self):
        grace_period = self.medicine.grace_period_days
        last_application = self.medicineapplication_set.order_by('date').last()
        if last_application is None:
            return self.start_date

        return last_application.date + timedelta(days=grace_period)


class MedicineApplication(models.Model):
    date = models.DateField()
    dosage = models.FloatField()
    treatment = models.ForeignKey(Treatment)


class MedicineEntry(models.Model):
    date = models.DateField()
    medicine = models.ForeignKey(Medicine)
    quantity = models.FloatField()
    expiration_date = models.DateField()
