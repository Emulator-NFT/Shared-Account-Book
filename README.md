# Shared-Account-Book


## Usage

```bash
$ pip install -r requirements.txt

$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py runserver
```
如果migrate出现错误，则先删除`db.splite3`

## TODO:
- 用户注册时，添加一个默认账本，添加一些收支类型
- 微信注册登录
- 用户头像
- 账本预算
- 规范user相关的请求url