
from rest_framework import serializers

from .models import EntryImage, Ledger, Entry, Category, Budget, LedgerMember


class LedgerSerializer(serializers.ModelSerializer):
    
    # entries = 'EntrySerializer(many=True, read_only=True)'
    entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 上面2种写法都行

    class Meta:
        model = Ledger
        # exclude = ('user',)
        fields = ('id', 'title', 'icon', 'date_created', 'description', 'year_budget', 'month_budget', 'entries')

class LedgerMemberSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = LedgerMember
        fields = ('id', 'ledger', 'member', 'role', 'nickname')
    def create(self, validated_data):
        ledger = validated_data['ledger']
        member = validated_data['member']
        role = validated_data['role']
        nickname = validated_data['nickname']
        # 检查当前用户是否已经是该账本的成员
        if LedgerMember.objects.filter(ledger=ledger, member=member).exists():
            raise serializers.ValidationError('Current user is already a member of this ledger')
        ledger_member = LedgerMember.objects.create(ledger=ledger, member=member, role=role, nickname=nickname)
        return ledger_member

class EntryImageSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = EntryImage
            fields = ('id', 'entry', 'image')

class EntrySerializer(serializers.ModelSerializer):
    
    # ledgers = LedgerSerializer(many=True, read_only=True)
    # 默认情况下，返回响应的ledgers字段只有id, 上面的代码可以返回完整的Ledger对象
    
    images = EntryImageSerializer(many=True, read_only=True) # 返回关联的图片
    
    class Meta:
        model = Entry
        exclude = ('user',)

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        # fields = ('id', 'name', 'icon', 'category_type')
        exclude = ('user',)

class BudgetSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = Budget
            exclude = ('user',)