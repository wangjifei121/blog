from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    name = forms.CharField(
        min_length=6,
        max_length=12,
        label="用户名",
        error_messages={
            "min_length": "用户名不能少于6位",
            "max_length": '用户名不能超过12位',
            "required": "用户名不能为空"
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"}
        )
    )
    pwd = forms.CharField(
        label="密码",
        error_messages={
            "required": "密码不能为空"
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},  # 给生成的标签添加属性
            render_value=True  # 返回报错信息的时候要不要展示密码
        )
    )


class RegisterForm(forms.Form):  # 类必须继承forms.Form
    # 用户名
    username = forms.CharField(
        min_length=6,  # 设置最小长度
        max_length=12,  # 设置最大长度
        label="用户名",  # 设置标签名
        # 错误信息提示设置
        error_messages={
            "min_length": "用户名不能少于6位",
            "max_length": '用户名不能超过12位',
            "required": "用户名不能为空"
        },
        # 插件设置
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"}  # 给生成的标签添加属性
        )
    )
    # 电话
    phone = forms.CharField(
        label="手机号",
        error_messages={
            "required": "手机号不能为空"
        },
        # 调用Form组件中的验证器来校验手机号
        validators=[RegexValidator(r'1[1-9][0-9]{9}', '手机号格式不正确')],
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control'},  # 给生成的标签添加类属性
        )
    )
    # 密码
    password = forms.CharField(
        label="密码",
        min_length=6,
        error_messages={
            "required": "密码不能为空",
            'min_length': '密码不能少于6位'
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},  # 给生成的标签添加属性
            render_value=True  # 返回报错信息的时候要不要展示密码
        )
    )
    # 二次密码校验
    re_password = forms.CharField(
        label="确认密码",
        min_length=6,
        error_messages={
            "required": "确认密码不能为空",
            'min_length': '确认密码不能少于六位'
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},  # 给生成的标签添加属性
            render_value=True  # 返回报错信息的时候要不要展示密码
        )
    )
    # 邮箱
    email = forms.CharField(
        label="邮箱",
        error_messages={
            "required": "邮箱不能为空",
        },
        # 调用Form组件中的验证器来校验邮箱
        validators=[RegexValidator(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', "邮箱格式不正确")],
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control'},  # 给生成的标签添加属性
        )
    )

    # 通过自定义一个clean_字段名的方法实现对Form表单特定字段的校验
    def clean_username(self):
        # 从cleaned_data中取出想要的数据
        value = self.cleaned_data.get("username")
        if "金瓶梅" in value:
            # 错误就抛异常
            raise ValidationError("不符合社会主义核心价值观！")
        else:
            return value

    # 通过Form表单的全局钩子函数来验证两次输入的密码是否正确
    # 该clean方法， 在每个字段都校验通过之后才调用执行
    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if re_password and password == re_password:
            # 判断正确就返回校验过后的数据
            return self.cleaned_data
        else:
            # 添加错误到add_error
            self.add_error('re_password', '两次密码不一致，请重新输入')
            # 主动抛出异常
            raise ValidationError('两次密码不一致，请重新输入')


