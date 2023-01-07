from django.core.validators import MaxValueValidator
from django.db import models

from services.tasks import set_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):
        if self.full_price != self.__full_price:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPE = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'discount'),
    )
    plan_type = models.CharField(choices=PLAN_TYPE, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):
        if self.discount_percent != self.__discount_percent:
            for subscription in self.subscriptions.all():
                set_price.delay(subscription.id)
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    price = models.PositiveIntegerField(default=0)
    objects = models.Manager()
