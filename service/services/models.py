from django.core.validators import MaxValueValidator
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()


class Plan(models.Model):
    PLAN_TYPE = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'discount'),
    )
    plan_type = models.CharField(choices=PLAN_TYPE, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])


class Subscription(models.Model):
    client = models.ForeignKey('clients.Client', on_delete=models.PROTECT, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
