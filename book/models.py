from django.db import models
from django.utils import timezone

from users.models import MyUser


# Create your models here.

# 账本
class Ledger(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)    
    title = models.CharField(max_length=20)
    icon = models.IntegerField(default=0, blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    description = models.CharField(max_length=100, blank=True, default='')  # 账本描述
    year_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)   # 年预算
    month_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 月预算
    
    def __str__(self):
        return self.title

# 账本 - 成员 中间模型
class LedgerMember(models.Model):
    ledger = models.ForeignKey(to=Ledger, on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='ledgers')

    ROLE_CHOICES = (
        ('owner', '账本主人'),
        ('admin', '管理员'),
        ('member', '普通成员'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member') # 权限
    nickname = models.CharField(max_length=20, blank=True)  # 昵称
    
    def __str__(self):
        return f"{self.ledger.title} - {self.member.username}"

# 收支类型
class Category(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, default=1)
    CATEGORY_TYPE = (
        ('income', '收入'),
        ('expense', '支出'),
    )
    name = models.CharField(max_length=20)  # 名称
    icon = models.IntegerField(default=1, blank=True)  # 图标
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPE, default='expense')  # 区分收入和支出类型

    def __str__(self):
        return self.name

# 收支图片
class EntryImage(models.Model):
    entry = models.ForeignKey(to='Entry', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')  # 图片
    def __str__(self):
        return f"Image for {self.entry.title}"

# 收支明细
class Entry(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, default=1)
    ENTRY_TYPE = (
        ('income', '收入'),
        ('expense', '支出'),
    )
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE, default='expense')
    title = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ledgers = models.ManyToManyField(to=Ledger, related_name='entries')
    category = models.ForeignKey(to=Category, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    notes = models.CharField(max_length=100, blank=True, null=True)  # 备注

    def __str__(self):
        return self.title

# 预算
class Budget(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, default=1)
    ledger = models.ForeignKey(to=Ledger, on_delete=models.CASCADE, default=1)
    # member = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, default=1, related_name='budgets')  # 成员预算
    # 一级预算: 总预算，年预算，季度预算，月预算，周预算，日预算
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    year = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quarter = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    week = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    day = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.ledger.title} - {self.total}"