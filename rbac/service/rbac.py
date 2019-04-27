from django.shortcuts import HttpResponse, render, redirect
from django.utils.deprecation import MiddlewareMixin
import re


class PermissionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # d当前路径
        current_path = request.path
        # 白名单，就是允许访问的
        white_url = ["/login/", "/index/", "/admin/*"]
        for reg in white_url:
            ret = re.search(reg, current_path)
            if ret:
                return None

        # 校验用户登录是否
        user = request.session.get("user")
        if not user:
            return redirect("/login/")

        # 权限认证
        permission_list = request.session.get("permission_list")
        for reg in permission_list:
            # 用正则表达式是因为编辑和删除
            reg = "^%s$" % reg
            ret = re.search(reg, current_path)
            if ret:
                return None
        return HttpResponse("您无权访问此页面！！！")
