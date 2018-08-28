from django import template
from blog import models
from datetime import datetime

register = template.Library()


@register.inclusion_tag(filename='left_menu.html')
def left_menu(username):
    # 通过用户信息找到当前用户的对象
    user_obj = models.UserInfo.objects.filter(username=username).first()
    # ORM操作查询当前用户对应的所有书籍
    article_list = models.Article.objects.filter(user=user_obj).order_by("create_time").reverse()
    # ORM操作查询当前用户对应的所有分类
    categorys = models.Category.objects.filter(blog=user_obj.blog)
    # ORM操作查询当前用户对应的blog的tags
    tags = models.Tag.objects.filter(blog=user_obj.blog)

    # 时间归档，通过对所有对象的create_time字段的处理，通过列表的去重和计数得到对应的前端数据
    date_list = [datetime.strftime(obj.create_time, '%Y-%m') for obj in article_list]
    list2 = list(set(date_list))
    list2.sort(key=date_list.index)
    ret_date_list = [(i, date_list.count(i)) for i in list2]

    # 对当前blog的所有文章按照年月 分组 查询
    # 1. models.Article.objects.filter(user=user_obj)                   --> 查询出当前作者写的所有文章
    # 2. .extra(select={"y_m": "DATE_FORMAT(create_time, '%%Y-%%m')"}   --> 将所有文章的创建时间格式化成年-月的格式，方便后续分组
    # 3. .values("y_m").annotate(c=Count("id"))                         --> 用上一步时间格式化得到的y_m字段做分组，统计出每个分组对应的文章数
    # 4. .values("y_m", "c")                                            --> 把页面需要的日期归档和文章数字段取出来
    # archive_list = models.Article.objects.filter(user=user_obj).extra(
    #     select={"y_m": "DATE_FORMAT(create_time, '%%Y-%%m')"}
    # ).values("y_m").annotate(c=Count("id")).values("y_m", "c")

    return {
        'username': username,
        'categorys': categorys,
        'tags': tags,
        'ret_date_list': ret_date_list,
    }
