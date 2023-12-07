
from rest_framework import serializers

from .models import EntryImage, Ledger, Entry, Category, Budget


class LedgerSerializer(serializers.ModelSerializer):
    
    # entries = 'EntrySerializer(many=True, read_only=True)'
    entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # 上面2种写法都行

    class Meta:
        model = Ledger
        # exclude = ('user',)
        fields = ('id', 'title', 'icon', 'date_created', 'description', 'year_budget', 'month_budget', 'entries')

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