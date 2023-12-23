from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'ledgers', views.LedgerViewSet)
router.register(r'entries', views.EntryViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'entry-images', views.EntryImageViewSet)
router.register(r'ledger-members', views.LedgerMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('entries/<int:pk>/review/', views.EntryViewSet.as_view({'patch': 'review'})),
    path('entries/<int:pk>/subreview/', views.EntryViewSet.as_view({'patch': 'subreview'})),
    path('ledgers/<int:pk>/analysis/', views.LedgerViewSet.as_view({'get': 'analysis'})),
]