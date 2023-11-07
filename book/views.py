from django.shortcuts import render
from rest_framework import viewsets, permissions

from .models import Ledger, Entry
from .serializers import LedgerSerializer, EntrySerializer

# Create your views here.

class LedgerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated] # TODO: IsOwnerOrReadOnly(permission)
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    
class EntryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

