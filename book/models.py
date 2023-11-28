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
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

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
    category = models.ForeignKey(to=Category, on_delete=models.SET_DEFAULT, default=1, blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    notes = models.CharField(max_length=100, blank=True, null=True)  # 备注

    def __str__(self):
        return self.title