import math


class Page:

    def __init__(self, total_num, page_num, url_prefix, every_page_num=10, show_page_num=9):
        """

        :param total_num: 数据库获取到的数据的总数
        :param page_num: 前端获取的页数
        :param url_prefix: 页码a标签的url前缀
        :param every_page_num: 自定义每页显示条数
        :param show_page_num: 显示分页数目
        """
        self.total_num = total_num
        self.page_num = page_num
        self.every_page_num = every_page_num
        self.show_page_num = show_page_num
        self.url_prefix = url_prefix
        self.page_tags_html = ''
        self.page_start_num = 0
        self.page_end_num = 0

        try:
            page_num = int(self.page_num)
        except:
            page_num = 1
        total_page_num = math.ceil(self.total_num / self.every_page_num)
        if page_num < 1:
            page_num = 1
        elif page_num > total_page_num:
            page_num = total_page_num
        # 当前页的开始数据
        self.page_start_num = (page_num - 1) * self.every_page_num
        # 当前页的结束数据
        self.page_end_num = (page_num) * self.every_page_num
        if total_page_num > self.show_page_num:
            start_page_num = page_num - (self.show_page_num // 2)
            end_page_num = page_num + (self.show_page_num // 2)
            if start_page_num < 1:
                start_page_num = 1
                end_page_num = self.show_page_num
            if end_page_num > total_page_num:
                end_page_num = total_page_num
                start_page_num = total_page_num - self.show_page_num
        else:
            start_page_num = 1
            end_page_num = total_page_num

        The_first_page = f'<li><a href="/{self.url_prefix}/?page=1">首页</a></li>'
        The_last_page = f'<li><a href="/{self.url_prefix}/?page={total_page_num}">尾页</a></li></ul></nav>'

        self.page_tags_html = f'<nav aria-label="Page navigation"> <ul class="pagination">{The_first_page}'
        for i in range(start_page_num, end_page_num + 1):
            if i == page_num:
                self.page_tags_html += f'<li class="active"><a href="/{self.url_prefix}/?page={i}">{i}</a></li>'
            else:
                self.page_tags_html += f'<li><a href="/{self.url_prefix}/?page={i}">{i}</a></li>'

        self.page_tags_html += The_last_page

    @property
    def start(self):
        return self.page_start_num

    @property
    def end(self):
        return self.page_end_num

    @property
    def html(self):
        return self.page_tags_html
