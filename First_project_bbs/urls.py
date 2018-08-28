"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from blog import views
from django.views.static import serve
from django.conf import settings
from blog import blogcenter_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.Login.as_view()),
    url(r'^home/$', views.Home.as_view()),
    # 正常验证码url
    url(r'^v_code/', views.v_code),
    url(r'^register/', views.Register.as_view()),
    # 给用户上传文件 配置一个处理的路由
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^logout/', views.logout),
    # ---------将个人中心的处理放在二级路由中--------
    url(r'^blogcenter/', include(blogcenter_urls)),
    # ----------文章详情-------------------
    url(r'^(\w+)/p/(\d+)/$', views.art_detail),
    # 点赞url
    url(r'^updown/$', views.updown),
    # 评论
    url(r'^comment/$', views.comment),
    # 初始展示url
    url(r'^$', views.Home.as_view()) ,
    url(r'^add_article/$',views.add_article),

]
# django-debug-toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
