from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import views
from blog.myforms.forms import LoginForm, RegisterForm
from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from blog import models
from django.views.decorators.cache import never_cache
from utils.page import Page
from django.db import transaction
from django.db.models import F
from bs4 import BeautifulSoup
import os
from First_project_bbs import settings


# Create your views here.
class Login(views.View):

    def get(self, request):
        login_obj = LoginForm()
        return render(request, 'login.html', {'login_obj': login_obj})

    def post(self, request):
        res = {'code': 0}
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        v_code = request.POST.get('v_code')
        # next = request.POST.get('next')
        # print(next)
        # 判断验证码是否正确
        if v_code.upper() != request.session.get('v_code', ''):
            res['code'] = 1
            res['err_msg'] = '您输入的验证码不正确'
        else:
            # 判断用户名密码是否正确
            user = auth.authenticate(username=name, password=pwd)
            if user:
                auth.login(request, user)
            else:
                res['code'] = 1
                res['err_msg'] = '用户名或密码错误'
        return JsonResponse(res)


class Home(views.View):
    def get(self, request):
        article_list = models.Article.objects.all()
        totol_num = article_list.count()
        page_num = request.GET.get("page", 1)
        # 分页实例化传参
        page_obj = Page(total_num=totol_num, page_num=page_num, url_prefix='home', every_page_num=2)
        # 根据分页拿到的start和end切片得到所要的数据
        data = article_list[page_obj.start:page_obj.end]
        # 调用html方法得到分页的html代码片段
        page_html = page_obj.html
        return render(request, 'home.html', {'article_list': data, 'page_html': page_html})


# 专门用来返回验证码图片的视图
# 返回响应的时候告诉浏览器不要缓存
@never_cache
def v_code(request):
    # 生成随机颜色的方法
    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 生成图片对象
    image_obj = Image.new(
        "RGB",  # 生成图片的模式
        (250, 35),  # 图片大小
        random_color()
    )
    # 生成一个准备写字的画笔
    draw_obj = ImageDraw.Draw(image_obj)  # 在哪里写
    font_obj = ImageFont.truetype("static/fonts/kumo.ttf",size=30)  # 加载本地的字体文件
    tmp = []
    for i in range(5):
        # 生成随机数字
        num = str(random.randint(0, 9))
        # 生成随机小写字母
        lowercase = chr(random.randint(65, 90))
        # 生成随机大写字母
        uppercase = chr(random.randint(97, 122))
        # 随机选择一种
        ret = random.choice([num, lowercase, uppercase])
        tmp.append(ret)
        # 每取出一次东西就写一次
        draw_obj.text(
            (i * 45 + 25, 0),  # 坐标
            ret,  # 内容
            fill=random_color(),
            font=font_obj
        )
    v_code = ''.join(tmp)
    request.session['v_code'] = v_code.upper()

    # # 加干扰线
    # width = 250  # 图片宽度（防止越界）
    # height = 35
    # for i in range(3):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=random_color())

    # 加干扰点
    # for i in range(40):
    #     draw_obj.point([random.randint(0, width), random.randint(0, height)], fill=random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=random_color())

    f = BytesIO()
    # 将生成的图片保存到内存中
    image_obj.save(f, 'png')
    # 从内存中读取图片数据
    data = f.getvalue()
    return HttpResponse(data, content_type='image/png')


class Register(views.View):  # 必须继承views.View
    # get请求方式
    def get(self, request):
        # 用自定义的Form类实例化一个对象，用于前端页面生成标签
        register_obj = RegisterForm()
        return render(request, 'register.html', {'register_obj': register_obj})

    # post请求方式
    def post(self, request):
        # 前后端交互信息
        res = {'code': 0}
        # 实例化form类，将前端得到的数据提交到实例中
        register_obj = RegisterForm(request.POST)
        # 利用form内置方法校验前端得到的数据
        if register_obj.is_valid():
            # 从数据库中查询用户输入的用户名，手机号，邮箱是否重复
            username = models.UserInfo.objects.filter(username=request.POST.get('username'))
            phone = models.UserInfo.objects.filter(phone=request.POST.get('phone'))
            email = models.UserInfo.objects.filter(email=request.POST.get('email'))
            if username:
                res['code'] = 1
                res['msg'] = '用户名已存在，请重新输入'
            elif phone:
                res['code'] = 2
                res['msg'] = '您输入的手机号已存在，请重新输入'
            elif email:
                res['code'] = 3
                res['msg'] = '您输入的邮箱号已存在，请重新输入'
            else:
                # 数据正确后剔除re_password中的数据
                register_obj.cleaned_data.pop("re_password")
                # 得到前端的头像文件，文件和图片数据存放在request.FILES中
                avatar_file = request.FILES.get('avatar_file')
                # 通过数据库操作创建user
                models.UserInfo.objects.create_user(**register_obj.cleaned_data, avatar=avatar_file)
                # 返回前端页面要跳转的url
                res['msg'] = '/login/'
        else:
            res['code'] = 4
            # 错误信息
            res['msg'] = register_obj.errors
        return JsonResponse(res)


def logout(request):
    # 注销用户
    auth.logout(request)
    return redirect('/login/')


def blogcenter(request, username, *args):
    # 通过用户信息找到当前用户的对象
    user_obj = models.UserInfo.objects.filter(username=username).first()
    # ORM操作查询当前用户对应的所有书籍
    article_list = models.Article.objects.filter(user=user_obj).order_by("create_time").reverse()

    if args:
        if args[0] == "category":
            # 表示按照文章分类查询
            article_list = article_list.filter(category__title=args[1])
        elif args[0] == "tag":
            # 表示按照文章的标签查询
            article_list = article_list.filter(tags__title=args[1])
        else:
            # 表示按照文章的日期归档查询
            try:
                year, month = args[1].split("-")
                article_list = article_list.filter(create_time__year=year).filter(create_time__month=month)
            except Exception as e:
                article_list = []

    # 分页
    page_num = request.GET.get("page", 1)
    totol_num = article_list.count()
    page_obj = Page(total_num=totol_num, page_num=page_num, url_prefix=f'blogcenter/{username}', every_page_num=5)
    print(page_obj.start)
    print(page_obj.end)
    article_list = article_list[page_obj.start:page_obj.end]
    page_html = page_obj.html

    return render(request, 'blogcenter.html',
                  {'username': username, 'article_list': article_list, 'page_html': page_html})


def art_detail(request, username, art_id):
    article_obj = models.Article.objects.filter(id=art_id).first()
    content = models.ArticleDetail.objects.filter(article=article_obj).first()
    comment_list = models.Comment.objects.filter(article=article_obj)
    return render(request, 'article.html', {
        'username': username,
        'article_obj': article_obj,
        'content': content,
        'comment_list': comment_list
    })


def updown(request):
    if request.method == "POST":
        res = {"code": 0}
        user_id = request.POST.get("userId")
        article_id = request.POST.get("articleId")
        is_up = request.POST.get("isUp")
        # 将前端得到的点赞或者反对转换成bool类型，方便接下来使用
        is_up = True if is_up.upper() == 'TRUE' else False
        # 5.不能给自己点赞
        article_obj = models.Article.objects.filter(id=article_id, user_id=user_id)
        if article_obj:
            # 表示是给自己写的文章点赞
            res["code"] = 1
            res["msg"] = '不能给自己的文章点赞！' if is_up else '不能反对自己的内容！'

        # 3.同一个人只能给同一篇文章点赞一次
        # 4.点赞和反对两个只能选一个
        # 判断一下当前这个人和这篇文章 在点赞表里有没有记录
        else:
            is_exist = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()
            if is_exist:
                ret = is_exist.is_up
                if ret == is_up:
                    with transaction.atomic():
                        is_exist.delete()
                        if is_up:
                            # 取消点赞数
                            models.Article.objects.filter(id=article_id).update(up_count=F('up_count') - 1)
                        else:
                            # 取消反对数
                            models.Article.objects.filter(id=article_id).update(down_count=F('down_count') - 1)
                    res["msg"] = '取消点赞成功' if is_up else '取消反对成功'
                    res["code"] = 2
                else:
                    res['code'] = 1
                    res['msg'] = '一人只能点赞或反对一次'

            else:
                # 真正点赞，事务操作，，
                with transaction.atomic():
                    # 1. 先创建点赞记录
                    models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id, is_up=is_up)
                    # 2. 再更新文章表
                    if is_up:
                        # 更新点赞数
                        models.Article.objects.filter(id=article_id).update(up_count=F('up_count') + 1)
                    else:
                        # 更新反对数
                        models.Article.objects.filter(id=article_id).update(down_count=F('down_count') + 1)
                res["msg"] = '点赞成功' if is_up else '反对成功'
        return JsonResponse(res)


def comment(request):
    res = {"code": 0}
    if request.method == "POST":

        article_id = request.POST.get("article_id")
        content = request.POST.get("content")
        user_id = request.user.id
        parent_id = request.POST.get("parent_id")

        # 创建评论内容
        with transaction.atomic():
            # 1. 先去创建新评论
            if parent_id:
                # 添加子评论
                comment_obj = models.Comment.objects.create(
                    content=content,
                    user_id=user_id,
                    article_id=article_id,
                    parent_comment_id=parent_id
                )
            else:
                # 添加父评论
                comment_obj = models.Comment.objects.create(
                    content=content,
                    user_id=user_id,
                    article_id=article_id
                )
            # 2. 去更新该文章的评论数
            models.Article.objects.filter(id=article_id).update(comment_count=F("comment_count") + 1)
            res["data"] = {
                "id": comment_obj.id,
                "content": comment_obj.content,
                "create_time": comment_obj.create_time.strftime("%Y-%m-%d %H:%M"),
                "username": comment_obj.user.username
            }
    return JsonResponse(res)


class Backend(views.View):

    def get(self, request):
        article_list = models.Article.objects.filter(user=request.user)
        return render(request, 'backend.html', {'article_list': article_list})


def add_article(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        categoryid = request.POST.get('categoryid')
        soup = BeautifulSoup(content, 'html.parser')
        script_list = soup.select('script')
        for i in script_list:
            i.decompose()

        with transaction.atomic():
            article_obj = models.Article.objects.create(
                title=title,
                desc=soup.text[:150],
                user=request.user,
                category_id=int(categoryid)
            )
            models.ArticleDetail.objects.create(
                content=soup.prettify(),
                article=article_obj
            )
        return redirect('/blogcenter/backend/')

    category_list = models.Category.objects.filter(blog__userinfo=request.user)
    return render(request, 'edit_article.html', {'category_list': category_list})


"""处理用户上传文章中的图片"""


def upload(request):
    res = {'error': 0}
    print(request.FILES)
    # 获取上传图片对象
    file_obj = request.FILES.get('imgFile')
    # 得到上传的图片的路径
    file_path = os.path.join(settings.MEDIA_ROOT, 'article_img', file_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    res['url'] = '/media/article_img/' + file_obj.name

    return JsonResponse(res)


def delete_article(request, article_id):
    try:
        article_id = int(article_id)
    except Exception:
        return HttpResponse('错误操作')
    article_obj = models.Article.objects.filter(id=article_id).first()
    if article_obj:
        article_obj.delete()
    else:
        return HttpResponse('文章不存在')
    return redirect('/blogcenter/backend')


class Edit_article(views.View):

    def get(self,request,article_id):
        article_obj = models.Article.objects.filter(id = article_id).first()
        print(article_obj)
        category_list = models.Category.objects.filter(blog__userinfo=request.user)
        return render(request, 'edit_article.html', {'category_list': category_list, "article_obj":article_obj})

    def post(self,request,article_id):
        new_title = request.POST.get('title')
        new_desc = request.POST.get('content')
        print(new_desc)
        categoryid = request.POST.get('categoryid')
        soup = BeautifulSoup(new_desc, 'html.parser')
        script_list = soup.select('script')
        for i in script_list:
            i.decompose()

        with transaction.atomic():
            article_obj = models.Article.objects.filter(id = article_id).update(
                title=new_title,
                desc=soup.text[:150],
                category_id=int(categoryid)
            )
            print(models.ArticleDetail.objects.filter(article = article_id))
            print('开始',soup.prettify(),'结束')
            models.ArticleDetail.objects.filter(article = article_id).update(
                content=soup.prettify(),
            )
        return redirect('/blogcenter/backend')