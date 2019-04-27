from django.shortcuts import render, HttpResponse, redirect
from rbac.models import User


# Create your views here.
def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        print(user)
        user = User.objects.filter(user=user, pwd=pwd).first()
        print(user)
        if user:
            # 要存储登录状态，保存
            request.session["user"] = user.user
            # 查询当前登录用户的所有权限url
            # print(user.roles.all().values("permission__url"))
            # < QuerySet[{'permission__url': '/stark/app01/oreder/'},
            # {'permission__url': '/stark/app01/oreder/add/'},
            # {'permission__url': '/stark/app01/school/'},
            # {'permission__url': '/stark/app01/school/add/'}] >
            permissions = user.roles.all().values("permission__url", "permission__code", "permission__title").distinct()
            permission_list = []
            permission_menu_list = []
            for item in permissions:
                # 取queryset里边的字典的值
                permission_list.append(item["permission__url"])

                if item["permission__code"] == "list":
                    permission_menu_list.append({
                        "url": item["permission__url"],
                        "title": item["permission__title"]
                    })
            # 将值也是权限列表存储到session中
            request.session["permission_list"] = permission_list
            # 将菜单权限列表注册到session
            request.session["permission_menu_list"] = permission_menu_list
            return redirect("/index/")
    return render(request, "login.html")


def index(request):
    return render(request, "index.html")