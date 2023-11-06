from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'ledgers', views.LedgerViewSet)
# router.register(r'entries', views.EntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]