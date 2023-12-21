from django.db import models
from django.utils import timezone

from users.models import MyUser


# Create your models here.

# 账本
class Ledger(models.Model):
    # user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)    
    # 通过中间模型LedgerMember来关联用户和账本
    title = models.CharField(max_length=20)
    icon = models.IntegerField(default=0, blank=True)
    # 账本类型
    LEDGER_TYPE = (
        ('personal', '个人账本'),
        ('family', '家庭账本'),
        ('group', '群组账本'),
    )
    ledger_type = models.CharField(max_length=10, choices=LEDGER_TYPE, default='personal')
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
        ('bot', '机器人'),
        ('owner', '账本主人'),
        ('admin', '管理员'),
        ('member', '普通成员'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member') # 角色权限
    nickname = models.CharField(max_length=20, blank=True, null=True)  # 昵称
    date_joined = models.DateTimeField(default=timezone.now, blank=True)  # 加入时间
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)  # 成员预算
    
    def __str__(self):
        return f"{self.ledger.title} - {self.member.username}"

# 收支类型
class Category(models.Model):
    # user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, default=1)
    ledger = models.ForeignKey(to=Ledger, on_delete=models.CASCADE, null=True, blank=False)
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
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, default=1)    # 谁记的账
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

    STATUS_CHOICES = (
        ('unreviewed', '未审核'),
        ('approved', '审核通过'),
        ('rejected', '审核不通过'),
    )
    review_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unreviewed')  # 审核状态
    review_notes = models.CharField(max_length=100, blank=True, null=True)  # 审核备注（为什么不通过）

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