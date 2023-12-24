from django.shortcuts import render
from rest_framework import viewsets, permissions, response, status
from django.db.models import Q, Func, Sum, Count
from .models import Ledger, LedgerMember, Entry, Category, Budget, EntryImage
from .serializers import EntryDetailSerializer, LedgerDetailSerializer, LedgerMemberSerializer, LedgerSerializer, EntrySerializer, CategorySerializer, BudgetSerializer, EntryImageSerializer
from .utils import create_default_categories
from users.models import MyUser
from django.utils import timezone
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
        bot_user = MyUser.objects.create_user_auto()
        LedgerMember.objects.create(ledger=ledger_instance, 
                                    member=bot_user, 
                                    role='bot', 
                                    nickname='机器人')

        # 创建账本时，自动创建默认分类
        create_default_categories(ledger_instance)

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
    
    # GET /api/ledgers/1/analysis/  返回账本分析数据
    def analysis(self, request, *args, **kwargs):
        instance = self.get_object()
        entries = instance.entries.all()
        year = request.query_params.get('year', timezone.now().year)
        month = request.query_params.get('month', None)
        entry_type = request.query_params.get('entry_type', 'expense')
        entries = entries.filter(entry_type=entry_type)

        # -------按月对比, 月度分析-前6个月, 年度分析-12个月----
        date_range = []
        monthly = []
        if month:
            date_range = [timezone.datetime(int(year), int(month), 1) - timezone.timedelta(days=i * 30) for i in range(6)]
        else:
            date_range = [timezone.datetime(int(year), 12, 1) - timezone.timedelta(days=i * 30) for i in range(12)]
        date_range = sorted(date_range)
        for date in date_range:
            month_amount = entries.filter(date_created__year=date.year,
                                        date_created__month=date.month).aggregate(total=Sum('amount'))['total'] or 0
            monthly.append({
                'year': date.year,
                'month': date.month,
                'total': month_amount
            })

        # ------月/年 收支-------
        if month:
            entries = entries.filter(date_created__year=year, date_created__month=month)
        else:
            entries = entries.filter(date_created__year=year)

        total = entries.aggregate(total=Sum('amount'))['total'] or 0    # 总支出
        count = entries.count()                                         # 总笔数

        # ------按类别统计收支总额和笔数------
        category_amount = entries.values('category').annotate(
            total=Sum('amount'),
            count=Count('id'),
            name = Func('category__name', function='upper'),
            icon = Func('category__icon', function='ABS'),
        )
        category_amount = sorted(category_amount, key=lambda x: abs(x['total']), reverse=True)
        category_amount = sorted(category_amount, key=lambda x: x['category'] is None)

        category_amount = [dict(x) for x in category_amount]
        for x in category_amount:
            if x['category'] is None:
                x['name'] = '其他'
                x['icon'] = 0
            del x['category']
        
        # 分类数量超过3个时，只显示前3个，其他合并为一个
        if len(category_amount) > 3:
            other = {
                'total': sum([x['total'] for x in category_amount[3:]]),
                'count': sum([x['count'] for x in category_amount[3:]]),
                'name': '其他',
                'icon': 0,
            }
            category_amount = category_amount[:3]
            category_amount.append(other)

        return response.Response({
            'total': total,
            'count': count,
            'category_amount': category_amount,
            'monthly': monthly
        }, status=status.HTTP_200_OK)


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
        member_username = request.data.get('member')
        member_user = MyUser.objects.filter(username=member_username).first()
        if not member_user:
            return response.Response({'detail': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['member'] = member_user.id
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
        
        # 如果请求用户是主人，可以删除任何人
        if user_member.role == 'owner':
            instance.delete()
            if instance.role == 'owner':
                # 如果删除的是主人，转移账本所有权给第一个成员(非机器人)
                new_owner = LedgerMember.objects.filter(ledger=instance.ledger).exclude(role='bot').first()
                if new_owner:
                    new_owner.role = 'owner'
                    new_owner.save()
                else:
                    instance.ledger.delete() # 如果没有其他成员，直接删除账本
            return response.Response(status=status.HTTP_204_NO_CONTENT)

        # 如果请求用户是管理员，可以删除普通成员和自己
        if user_member.role == 'admin':
            if instance == user_member: # 删除自己
                instance.delete()
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            elif instance.role == 'member': # 删除普通成员
                instance.delete()
                return response.Response(status=status.HTTP_204_NO_CONTENT)
        # 如果请求用户是普通成员，只能删除自己
        if user_member.role == 'member':
            if instance == user_member:
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
            
            ledger_member = LedgerMember.objects.filter(ledger=ledger, member=self.request.user).first()
            ledger_instance = Ledger.objects.filter(id=ledger).first()
            # 对于群组账本，需要根据审核状态过滤
            if ledger_member and ledger_instance.ledger_type == 'group':
                if ledger_member.role == 'member':
                    # 普通成员只能看到审核通过的 或者 自己的
                    self.queryset = self.queryset.filter(
                        Q(review_status='approved') |
                        Q(user=self.request.user)
                    )

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
            
        # 指定成员
        member = self.request.query_params.get('member')
        if member:
            self.queryset = self.queryset.filter(user=member)
        # 指定审核状态
        review_status = self.request.query_params.get('review_status')
        if review_status:
            self.queryset = self.queryset.filter(review_status=review_status)
        
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

    # PATCH /api/entries/1/review/  审核收支
    def review(self, request, *args, **kwargs):
        instance = self.get_object()    # Entry Instance
        ledger_instance = instance.ledgers.filter(ledger_type='group').first() # Ledger Instance
        user = self.request.user
        user_member = LedgerMember.objects.get(ledger=ledger_instance, member=user)
        # 只有主人和管理员可以审核
        if not user_member or user_member.role not in ('owner', 'admin'):
            return response.Response({'detail': 'Only owner and admin can review entries'}, status=status.HTTP_403_FORBIDDEN)
        instance.review_status = request.data.get('review_status', instance.review_status)
        instance.review_notes = request.data.get('review_notes', instance.review_notes)
        instance.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    
    # PATCH /api/entries/1/subreview/  将收支设置为待审核, 用于管理员审核不通过后，让用户重新提交
    def subreview(self, request, *args, **kwargs):
        instance = self.get_object()    # Entry Instance
        ledger_instance = instance.ledgers.filter(ledger_type='group').first()
        user = self.request.user
        if user != instance.user:
            return response.Response({'detail': 'You are not the creator of this entry'}, status=status.HTTP_403_FORBIDDEN)
        user_member = LedgerMember.objects.get(ledger=ledger_instance, member=user)
        if not user_member:
            return response.Response({'detail': 'You are not a member of the group ledger'}, status=status.HTTP_403_FORBIDDEN)
        instance.review_status = 'unreviewed'
        instance.review_notes = None
        instance.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    
    

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    def get_queryset(self):
        # self.queryset = self.queryset.filter(user=self.request.user)
        ledger = self.request.query_params.get('ledger')
        if ledger:
            self.queryset = self.queryset.filter(ledger=ledger)
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