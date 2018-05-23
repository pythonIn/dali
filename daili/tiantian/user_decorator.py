# coding:utf-8


# 判断是否登入。

from django.http import HttpResponseRedirect   # 转向

from django.shortcuts import redirect  # 转向


# 装饰器，func使用装饰的函数， 附加功能， 如当前：满足该装饰条件就执行该函数。
def login(func):
    def user_login(requset,*args, **kwargs):
        if requset.session.has_key('user_id'): # 判断session中是否有用户id，
            return func(requset, *args, **kwargs) # 有的话就把函数返回。执行该函数，不定长参数

        else:  # 否则重定向于登入页面，并把当前页面保存到cookie中，登入成功后转入到cookie保存的页面
            red = HttpResponseRedirect('/user/login')# 只能页面刷新时候可使用重定向，局部刷新则不行
            red.set_cookie('url', requset.get_full_path()) # 设置当前完整路径在cookie键中，完整路径是包括后面的get请求
            return red # 返回
    return user_login