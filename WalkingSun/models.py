from django.db import models


# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    count = models.IntegerField(verbose_name="人数")

    class Meta:
        db_table = 'department'


class UserInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    email = models.EmailField(verbose_name="邮箱")
    # 后期增加一列 第一种方法可以为空 null=True blank=Ture
    # 第二种方法 默认值 default='1111'
    pwd = models.CharField(verbose_name="密码", max_length=100, default='0')

    class Meta:
        db_table = 'user_info'
