from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'ledgers', views.LedgerViewSet)
router.register(r'entries', views.EntryViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'entry_images', views.EntryImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]