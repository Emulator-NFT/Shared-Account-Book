from django.shortcuts import render
from rest_framework import viewsets, permissions
from django.db.models import Q, Func
from .models import Ledger, Entry, Category, Budget
from .serializers import LedgerSerializer, EntrySerializer, CategorySerializer, BudgetSerializer

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
        # 指定分类
        category = self.request.query_params.get('category')
        if category:
            self.queryset = self.queryset.filter(category=category)
        # 指定时间范围, ISO 8601 格式, YYYY-MM-DD, 例如: 2023-11-28
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        date_to = date_to + ' 23:59:59' if date_to else None    # 日期范围包含当天
        if date_from and date_to:
            self.queryset = self.queryset.filter(date_created__range=(date_from, date_to))
        elif date_from:
            self.queryset = self.queryset.filter(date_created__gte=date_from)
        elif date_to:
            self.queryset = self.queryset.filter(date_created__lte=date_to)
        # 指定金额范围
        amount_from = self.request.query_params.get('amount_from')
        amount_to = self.request.query_params.get('amount_to')
        amount_from = float(amount_from) if amount_from else None
        amount_to = float(amount_to) if amount_to else None
        if amount_from and amount_to:
            self.queryset = self.queryset.annotate(abs_amount=Func('amount', function='ABS')).filter(abs_amount__range=(abs(amount_from), abs(amount_to)))
            # self.queryset = self.queryset.filter(amount__range=(abs(amount_from), abs(amount_to)))
        elif amount_from:
            self.queryset = self.queryset.annotate(abs_amount=Func('amount', function='ABS')).filter(abs_amount__gte=abs(amount_from))
            # self.queryset = self.queryset.filter(amount__gte=abs(amount_from))
        elif amount_to:
            self.queryset = self.queryset.annotate(abs_amount=Func('amount', function='ABS')).filter(abs_amount__lte=abs(amount_to))
            # self.queryset = self.queryset.filter(amount__lte=abs(amount_to))
        
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


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)

        category_type = self.request.query_params.get('category_type')
        if category_type:
            self.queryset = self.queryset.filter(category_type=category_type)
        return self.queryset
    
class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user)
        ledger = self.request.query_params.get('ledger')
        if ledger:
            self.queryset = self.queryset.filter(ledger=ledger)
        return self.queryset