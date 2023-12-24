# 部署环境用settings_prod

from acount_book.settings import *

DEBUG = False

CONTAINER_BASE_URL = 'http://app:8000'  # app: 容器HOST
REMOTE_BASE_URL = 'http://43.140.204.155:8000' # 服务器IP

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "thss",
        "USER": "root",
        "PASSWORD": "2020010548",
        "HOST": "db",
        "PORT": "3306",
    }
}