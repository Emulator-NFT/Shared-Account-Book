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
![note]用户只会根据账本ID获取收支列表
所有的请求应该基于账本

【下午问一下它们这些请求URL有没有作全局变量】
- [ ] API重构
1. 账本
GET /ledgers/ 返回账本列表(仅ID)
POST /ledgers/ 新建账本
GET /ledgers/{id}/ 查看账本
PUT /ledgers/{id}/ 修改账本
1. 收支
GET /ledgers/{id}/entries/ 返回收支列表(仅ID)
POST /ledgers/{id}/entries/ 新建收支
GET /ledgers/{id}/entries/{id}/ 查看收支
PUT /ledgers/{id}/entries/{id}/ 修改收支
1. 成员
GET /ledgers/{id}/members/ 返回成员列表
POST /ledgers/{id}/members/ 新建成员
GET /ledgers/{id}/members/{id}/ 查看成员信息

- [ ] 所属问题
模型LedgerMember存储Ledger和User的多对多关系
如果是个人账本，则该Ledger只有一个User
按照这样思考，其实个人账本、家庭账本、团体账本没有区别

- [ ] 访问权限问题
1. 判断当前请求的user是否位于当前账本
2. 判断它的role是管理员、主人、普通成员

- [ ] 收支管理
1. Entry应该只和Ledger关联
2. user字段之前的含义失效
3. 需要增加一个【成员】字段，用于区分团体帐本中收支是由谁创建，可以沿用之前的user字段
4. 收支不关联到用户？但是user是外键不能设置为null，如果真要实现，可以将收支归类到主人，（感觉这个不好弄，要不不弄了）
5. 我感觉，Entry直接关联到LedgerMember是不是更好（但它是中间模型，感觉没必要）

- [ ] 成员管理
1. 修改成员信息的权限问题，普通成员只能修改自己的信息，管理员能修改其他人的信息
2. 主人转让：主动转让，退出自动转让

- [ ] 问题
1. 一条收支a同步到账本A B C，则A B C关联到同一个a，如果此时账本A中成员修改a，那么B C也会修改；还是说在A B C中分别建立a的副本；
（目前是前者），存在问题：假如用户u在A中但不在B中，如果A修改了a，B中的a也会修改
应该调整模型Entry的ledger字段，多对多改为外键
2. 收支不关联到用户？但是user是外键不能设置为null，如果真要实现，可以将收支归类到主人，（感觉这个不好弄，要不不弄了）
3. URL有没有作全局变量

TODO：下午问一下有没有人用到Entry的ledgers字段，应该在新建收支的时候会用到，