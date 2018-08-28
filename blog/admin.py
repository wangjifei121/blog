from django.contrib import admin

# Register your models here.
from blog import models


class UserInfo(admin.ModelAdmin):
    list_display = ("username", "phone", "email", 'blog')
    list_display_links = ['username', 'phone', 'email']
    list_filter = ['username', 'phone']  # 一般列表里面存放的字段都是一对多的字段，要不然就没什么意义了
    search_fields = ["username", 'phone']


admin.site.register(models.UserInfo, UserInfo)


class ArticleAction(admin.ModelAdmin):
    list_display = ['title', 'user']
    list_select_related = False

    def func(self, request, queryset):
        queryset.delete()

    func.short_description = "快捷删除选中项"
    actions = [func, ]
    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False
    # 是否显示选择个数
    actions_selection_counter = True


admin.site.register(models.Article, ArticleAction)
admin.site.register(models.Article2Tag)
admin.site.register(models.ArticleDetail)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
