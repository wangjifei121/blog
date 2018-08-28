from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^backend/$',views.Backend.as_view()),
    url(r'^upload/$',views.upload),
    url(r'^delete_article/(\d+)$',views.delete_article),
    url(r'^edit_article/(\d+)$',views.Edit_article.as_view()),
    url(r'^(\w+)/$', views.blogcenter),
    url(r'^(\w+)/(category|tag|archive)/(.*)/$', views.blogcenter),


]
