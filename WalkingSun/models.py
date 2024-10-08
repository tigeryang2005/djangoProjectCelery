from django.contrib.auth.models import AbstractUser, User

from django.db import models


# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    count = models.IntegerField(verbose_name="人数")
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table = 'department'


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    age = models.IntegerField(verbose_name="年龄", default=0, blank=True)
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号', blank=True)
    department = models.ForeignKey(verbose_name='所在部门', to=Department, on_delete=models.CASCADE)

    # department = models.ForeignKey(verbose_name='所在部门', to=Department, on_delete=models.SET_NULL, null=True,
    # blank=True)
    # department = models.ForeignKey(verbose_name='所在部门', to=Department, on_delete=models.SET_DEFAULT, default=1)

    # name = models.CharField(max_length=100, verbose_name="姓名")
    # email = models.EmailField(verbose_name="邮箱")
    # 后期增加一列 第一种方法可以为空 null=True blank=Ture
    # 第二种方法 默认值 default='1111'
    # pwd = models.CharField(verbose_name="密码", max_length=100, default='0')

    class Meta:
        verbose_name_plural = "用户信息"
        verbose_name = "用户信息"
        db_table = 'user_profile'
