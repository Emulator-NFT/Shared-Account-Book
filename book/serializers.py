
from rest_framework import serializers
from datetime import datetime
from .models import EntryImage, Ledger, Entry, Category, Budget, LedgerMember

class LedgerMemberSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = LedgerMember
        fields = '__all__'
        # read_only_fields = ('id', 'ledger', 'member')
    
    def create(self, validated_data):
        user = self.context['request'].user
        user_member = LedgerMember.objects.get(ledger=validated_data['ledger'], member=user)
        # 只有主人可以添加成员
        if not user_member or user_member.role != 'owner':
            raise serializers.ValidationError('Only owner can add members')
        ledger = validated_data['ledger']
        member = validated_data['member']
        # 检查当前用户是否已经是该账本的成员
        if LedgerMember.objects.filter(ledger=ledger, member=member).exists():
            raise serializers.ValidationError('Current user is already a member of this ledger')
        ledger_member = LedgerMember.objects.create(ledger=ledger, member=member, nickname=member.nickname)
        return ledger_member
    
    def update(self, instance, validated_data):
        # 不处理ledger和member的修改
        user = self.context['request'].user   # 当前请求的用户
        user_member = LedgerMember.objects.get(ledger=instance.ledger, member=user)  # 当前用户在该账本中的信息
        # 如果user不在该账本中，不允许修改
        if not user_member:
            raise serializers.ValidationError('Current user is not a member of this ledger')
        # 任何人只能修改自己的nickname
        if user_member == instance:
            instance.nickname = validated_data.get('nickname', instance.nickname)
            instance.save()

        # 只有主人可以修改其他成员的role, 但是不能修改自己的role
        if user_member.role == 'owner' and user_member != instance:
            instance.role = validated_data.get('role', instance.role)
            instance.save()
            # 如果有新主人，旧主人变为管理员
            if instance.role == 'owner':
                old_owner = user_member # 旧主人, 不直接使用user_member，因为后面还要用到user_member的role
                old_owner.role = 'admin'
                old_owner.save()

        # 群主和管理员可以修改成员的budget和nickname
        if user_member.role in ('owner', 'admin'):
            instance.budget = validated_data.get('budget', instance.budget)
            instance.save()

        return instance


# List获取账本列表时，只返回简单的信息
class LedgerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ledger
        fields = '__all__'

# Retrieve获取单个账本时，返回更详细的信息，包括关联的entries和members
class LedgerDetailSerializer(serializers.ModelSerializer):
        
        # entries = 'EntrySerializer(many=True, read_only=True)'
        entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)   # 只返回id
        # members = LedgerMemberSerializer(many=True, read_only=True) # 返回关联的LedgerMember对象的详细信息
        
        # 返回已用预算
        used_year_budget = serializers.SerializerMethodField()
        used_month_budget = serializers.SerializerMethodField()

        def get_used_year_budget(self, obj):
            current_year = datetime.now().year
            entries = obj.entries.filter(date_created__year=current_year)
            entries = entries.filter(entry_type='expense')
            return abs(sum([entry.amount for entry in entries]))
        
        def get_used_month_budget(self, obj):
            current_month = datetime.now().month
            entries = obj.entries.filter(date_created__month=current_month)
            entries = entries.filter(entry_type='expense')
            return abs(sum([entry.amount for entry in entries]))
        
        class Meta:
            model = Ledger
            fields = '__all__'
            

class EntryImageSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = EntryImage
            fields = ('id', 'entry', 'image')

# @List
class EntrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Entry
        exclude = ('notes', 'review_notes')

# @Retrieve
class EntryDetailSerializer(serializers.ModelSerializer):
        
    images = EntryImageSerializer(many=True, read_only=True)    # 返回关联的图片
    class Meta:
        model = Entry
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        # fields = ('id', 'name', 'icon', 'category_type')
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Budget
            exclude = ('user',)