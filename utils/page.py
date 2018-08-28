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
        self.start_page_num = 1
        self.end_page_num = 1
        try:
            self.page_num = int(self.page_num)
        except:
            self.page_num = 1
        # 通过向上取整计算出数据的总页数
        self.total_page_num = math.ceil(self.total_num / self.every_page_num)
        if self.total_page_num:
            # 判断从前端得到的页码数是否小于1，小于1就重置为1
            if self.page_num < 1:
                self.page_num = 1
            # 判断从前端得到的页码数是否大于总页码数，大于就重置为最大页码数
            elif self.page_num > self.total_page_num:
                self.page_num = self.total_page_num
            # 当前页的开始数据
            self.page_start_num = (self.page_num - 1) * self.every_page_num
            # 当前页的结束数据
            self.page_end_num = (self.page_num) * self.every_page_num
            # 判断总页码数和要展示的页数，如果总页码数大于要展示的页码数就展示对应的页数否则有多少页就展示多少页
            if self.total_page_num > self.show_page_num:
                self.start_page_num = self.page_num - (self.show_page_num // 2)
                self.end_page_num = self.page_num + (self.show_page_num // 2)
                if self.start_page_num < 1:
                    self.start_page_num = 1
                    self.end_page_num = self.show_page_num
                if self.end_page_num > self.total_page_num:
                    self.end_page_num = self.total_page_num
                    self.start_page_num = self.total_page_num - self.show_page_num
            else:
                self.start_page_num = 1
                self.end_page_num = self.total_page_num

    @property
    def start(self):
        return self.page_start_num

    @property
    def end(self):
        return self.page_end_num

    @property
    def html(self):
        pre_page_num = self.page_num - 1 if self.page_num > 1 else self.page_num
        next_page_num = self.page_num + 1 if self.page_num < self.total_page_num else self.total_page_num
        The_first_page = f'<li><a href="/{self.url_prefix}/?page=1">首页</a>' \
                         f'</li><li><a href="/{self.url_prefix}/?page={pre_page_num}">&laquo;</a></li>'
        The_last_page = f'<li><a href="/{self.url_prefix}/?page={next_page_num}">&raquo;</a></li>' \
                        f'<li><a href="/{self.url_prefix}/?page={self.total_page_num}">尾页</a></li></ul></nav>'

        self.page_tags_html = f'<nav aria-label="Page navigation"> <ul class="pagination">{The_first_page}'
        for i in range(self.start_page_num, self.end_page_num + 1):
            if i == self.page_num:
                self.page_tags_html += f'<li class="active"><a href="/{self.url_prefix}/?page={i}">{i}</a></li>'
            else:
                self.page_tags_html += f'<li><a href="/{self.url_prefix}/?page={i}">{i}</a></li>'

        self.page_tags_html += The_last_page

        return self.page_tags_html
