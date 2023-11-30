from book.models import Category

def create_default_categories(user):
    default_categories = [
        {'name': '工资', 'icon': 1, 'category_type': 'income'},
        {'name': '奖金', 'icon': 2, 'category_type': 'income'},
        {'name': '兼职', 'icon': 3, 'category_type': 'income'},
        {'name': '理财', 'icon': 4, 'category_type': 'income'},
        {'name': '礼金', 'icon': 5, 'category_type': 'income'},
        {'name': '餐饮', 'icon': 6, 'category_type': 'expense'},
        {'name': '购物', 'icon': 7, 'category_type': 'expense'},
        {'name': '服饰', 'icon': 8, 'category_type': 'expense'},
        {'name': '日用', 'icon': 9, 'category_type': 'expense'},
        {'name': '交通', 'icon': 10, 'category_type': 'expense'},
        {'name': '娱乐', 'icon': 11, 'category_type': 'expense'},
        {'name': '通讯', 'icon': 12, 'category_type': 'expense'},
        {'name': '住房', 'icon': 13, 'category_type': 'expense'},
        {'name': '水电', 'icon': 14, 'category_type': 'expense'},
        {'name': '燃气', 'icon': 15, 'category_type': 'expense'},
        {'name': '物业', 'icon': 16, 'category_type': 'expense'},
        {'name': '旅行', 'icon': 17, 'category_type': 'expense'},
        {'name': '学习', 'icon': 18, 'category_type': 'expense'},
        {'name': '医疗', 'icon': 19, 'category_type': 'expense'},
        {'name': '捐赠', 'icon': 20, 'category_type': 'expense'},
        {'name': '礼物', 'icon': 21, 'category_type': 'expense'},
        {'name': '转账', 'icon': 22, 'category_type': 'expense'},
    ]
    for category in default_categories:
        Category.objects.create(user=user, **category)