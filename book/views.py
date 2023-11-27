from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.db.models import Q
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
        self.queryset = self.queryset.filter(user=self.request.user)
        
        # 指定账本ID
        ledger = self.request.query_params.get('ledger')
        if ledger:
            self.queryset = self.queryset.filter(ledgers__id=ledger)
        # 指定收支类型
        entry_type = self.request.query_params.get('entry_type')
        if entry_type:
            self.queryset = self.queryset.filter(entry_type=entry_type)
        
        # 搜索, 查询标题或备注
        search = self.request.query_params.get('search')
        if search:
            self.queryset = self.queryset.filter(
                Q(title__icontains=search) | 
                Q(notes__icontains=search)
            )
        
        # 排序参数, 默认按id排序
        ordering = self.request.query_params.get('ordering', 'id')
        if ordering in ('id', '-id', 'date_created', '-date_created'):
            self.queryset = self.queryset.order_by(ordering)
        elif ordering in ('amount', '-amount'): # 因为金额有正有负，所以需要按绝对值排序
            self.queryset = self.queryset.extra(select={'abs_amount': 'ABS(amount)'}).order_by('abs_amount' if ordering == 'amount' else '-abs_amount')
        return self.queryset


