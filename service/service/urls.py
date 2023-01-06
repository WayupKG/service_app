from django.contrib import admin
from django.urls import path
from rest_framework import routers

from services.views import SubscriptionView

urlpatterns = [
    path('admin/', admin.site.urls),
]

route = routers.DefaultRouter()
route.register(r'api/subscriptions', SubscriptionView)

urlpatterns += route.urls
