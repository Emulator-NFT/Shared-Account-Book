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

- [ ] 添加收支时，增加选项将收支归入机器人门下
- [ ] 删除账本时，删除所有机器人（通过外键设置了on_delete会自动删除）
- [ ] 删除账本成员时，将其收支都删除
- [ ] 通知类
- [ ] 邀请类（邀请加入群组）



[软件工程项目进度文档](https://docs.qq.com/doc/DWm9kR1NKSmtnbmdx)

