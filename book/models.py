from django.db import models
from django.utils import timezone

from users.models import MyUser


# Create your models here.

class Ledger(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)    
    title = models.CharField(max_length=20)
    icon = models.IntegerField(default=0, blank=True)
    date_created = models.DateTimeField(default=timezone.now, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class Entry(models.Model):
    user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)             # 金额 单位：分, 正入，负出
    ledgers = models.ManyToManyField(to=Ledger, related_name='entries')
    category = models.IntegerField(default=0, blank=True) # 0: 其他, 1: 充值缴费, 2: 交通出行
    date_created = models.DateField(default=timezone.now, blank=True)
    tags = models.CharField(max_length=100, blank=True, null=True)   # 标签, 多个标签用逗号分隔
    notes = models.CharField(max_length=100, blank=True, null=True)  # 备注
    # TODO: 备注新建一个表，可以添加文字和图片

    def __str__(self):
        return self.title