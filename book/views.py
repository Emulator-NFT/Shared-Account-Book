from django.shortcuts import render
from rest_framework import viewsets, permissions, response, status
from django.db.models import Q, Func
from .models import Ledger, LedgerMember, Entry, Category, Budget, EntryImage
from .serializers import EntryDetailSerializer, LedgerDetailSerializer, LedgerMemberSerializer, LedgerSerializer, EntrySerializer, CategorySerializer, BudgetSerializer, EntryImageSerializer

# Create your views here.

class LedgerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated] # TODO: IsOwnerOrReadOnly(permission)
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    def perform_create(self, serializer):
        ledger_instance =  serializer.save()
        # 创建账本时，自动创建账本成员：主人和机器人
        LedgerMember.objects.create(ledger=ledger_instance, 
                                    member=self.request.user, 
                                    role='owner', 
                                    nickname=self.request.user.username)
        # TODO: 创建机器人账本成员
        # bot_user = MyUser.objects.create
        # LedgerMember.objects.create(ledger=ledger_instance,
        #                             member=self.request.user,
        #                             role='bot',
        #                             nickname='机器人')

    def get_queryset(self):
        self.queryset = self.queryset.filter(members__member=self.request.user)
        # 按照账本类型过滤
        ledger_type = self.request.query_params.get('ledger_type')
        if ledger_type:
            # 必须是 "personal", "family", "group" 之一
            ledger_type = ledger_type if ledger_type in ('personal', 'family', 'group') else 'personal'
            self.queryset = self.queryset.filter(ledger_type=ledger_type)
        
        return self.queryset
    
    def get_serializer_class(self):
        # GET /api/ledgers/1/   返回详细信息
        if self.action == 'retrieve':   
            return LedgerDetailSerializer
        return LedgerSerializer


class LedgerMemberViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LedgerMember.objects.all()
    serializer_class = LedgerMemberSerializer
    
    def get_queryset(self):
        # 只返回当前用户参与的账本
        user_ledgers = self.queryset.filter(member=self.request.user).values_list('ledger', flat=True)
        self.queryset = self.queryset.filter(ledger__in=user_ledgers)

        # 按照账本ID过滤
        ledger = self.request.query_params.get('ledger')
        if ledger:
            self.queryset = self.queryset.filter(ledger=ledger)
        
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return response.Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return response.Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        user_member = LedgerMember.objects.get(ledger=instance.ledger, member=user)
        # 如果user不在该账本中，不允许修改
        if not user_member:
            return response.Response({'detail': 'Current user is not a member of this ledger'}, status=status.HTTP_400_BAD_REQUEST)
        # 任何人都可以删除自己，主人可以删除其他成员
        if user == instance.member or user_member.role == 'owner':
            # 如果主人把自己删除了，那么转移账本所有权给第一个成员(非机器人)
            if user_member == instance:
                new_owner = LedgerMember.objects.filter(ledger=instance.ledger, role__ne='bot').first()
                if new_owner:
                    new_owner.role = 'owner'
                    new_owner.save()
                else:
                    # 如果没有其他成员，直接删除账本和机器人
                    instance.ledger.delete()
                    # TODO: 删除机器人
            instance.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        
        return response.Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

class EntryImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EntryImage.objects.all()
    serializer_class = EntryImageSerializer
    
    def get_queryset(self):
        # self.queryset = self.queryset.filter(entry__user=self.request.user) # 只能查看自己的图片
        entry = self.request.query_params.get('entry')
        if entry:
            self.queryset = self.queryset.filter(entry=entry)
        return self.queryset


class EntryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # GET /api/entries/1/   返回详细信息
        if self.action == 'retrieve':   
            return EntryDetailSerializer
        return EntrySerializer

    def get_queryset(self):
        # self.queryset = self.queryset.filter(user=self.request.user)
        
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
        
        # 搜索, 查询标题、备注、或类型名称
        search = self.request.query_params.get('search')
        if search:
            self.queryset = self.queryset.filter(
                Q(title__icontains=search) |
                Q(notes__icontains=search) |
                Q(category__name__icontains=search)
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