import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator, FileExtensionValidator

# Create your models here.

class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')

        # if not email:
        #     raise ValueError('The given email must be set')
        
        user: MyUser = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(username, email, password, **extra_fields)
    
    # 通过openid创建用户, 自动生成账号密码
    def create_user_with_openid(self, openid):
        # 自动生成用户名
        username = str(uuid.uuid4())[:15]
        while self.filter(username=username).exists():
            username = str(uuid.uuid4())[:15]
        # password = str(uuid.uuid4())[:20]
        user: MyUser = self.model(openid=openid, username=username, email=None)
        user.save(using=self._db)
        return user




class MyUser(AbstractBaseUser, PermissionsMixin):

    openid = models.CharField(max_length=255, null=True, blank = True) # 微信openid
    username_validator = RegexValidator(regex=r'^[a-zA-Z0-9_]+$', message='用户名只能包含字母、数字和下划线')
    username = models.CharField(max_length=20, unique=True, validators=[username_validator])
    nickname = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_validator = RegexValidator(regex=r'^[0-9]{11}$', message='手机号码格式错误')
    phone = models.CharField(max_length=11, null=True, blank=True, validators=[phone_validator])
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    date_joined = models.DateTimeField(default=timezone.now, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects:MyUserManager = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    # def has_perm(self, perm, obj=None):
    #     return True
    # def has_module_perms(self, app_label: str) -> bool:
    #     return super().has_module_perms(app_label)

    # def save(self, *args, **kwargs):
    #     # Perform custom file processing here
    #     super().save(*args, **kwargs)