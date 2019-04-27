from django.db import models


# Create your models here.
# 用户信息表
class User(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role")

    def __str__(self):
        return self.user


# 角色信息表
class Role(models.Model):
    title = models.CharField(max_length=32)
    permission = models.ManyToManyField("Permission")

    def __str__(self):
        return self.title


# 权限表
class Permission(models.Model):
    url = models.CharField(max_length=128)
    title = models.CharField(max_length=32)
    code = models.CharField(max_length=32, default="list")

    def __str__(self):
        return self.title