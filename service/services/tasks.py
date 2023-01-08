from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F

from service.celery import app

"""
select_for_update() - блокирует эту таблицу что бы пока он не закончил действие другие не могли изменить данные
"""


@shared_task(base=Singleton)
def set_price(subscription_id):
    from services.models import Subscription

    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotate_price=F('service__full_price') - F('service__full_price') * (F('plan__discount_percent') / 100.00)
        ).first()
        subscription.price = subscription.annotate_price
        subscription.save()

