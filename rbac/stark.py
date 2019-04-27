from .models import *
from stark.service.sites import site,ModelStark

site.register(User)
site.register(Role)


class PermissionConfig(ModelStark):
    list_display = ["title","url","code"]


site.register(Permission, PermissionConfig)