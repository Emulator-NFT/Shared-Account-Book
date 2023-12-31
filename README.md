# Shared-Account-Book


## Usage

```bash
$ pip install -r requirements.txt

$ python manage.py makemigrations
$ python manage.py migrate

$ python manage.py runserver
```
如果migrate出现错误，则先删除`db.splite3`

## 测试

指定test文件
```bash
$ coverage run ./users/tests.py
$ coverage run ./book/tests.py
```

自动检测test文件
```bash
$ coverage run -m unittest discover
```

覆盖率分析
```bash
$ coverage report [-m]
```

## 部署
```bash
$ docker-compose up
```

服务器: [http://43.140.204.155:8000/](http://43.140.204.155:8000/)

[软件工程项目进度文档](https://docs.qq.com/doc/DWm9kR1NKSmtnbmdx)

