import os
import django
from celery import Celery
from django.conf import settings

# 设置系统环境变量，安装django，必须设置，否则在启动celery时会报错
# djangoProjectCelery 是当前项目名
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectCelery.settings')
django.setup()
# 实例化一个celery类
celery_app = Celery('djangoProjectCelery')
# 指定celery配置文件位置
celery_app.config_from_object('django.conf:settings')
# 自动从setting的配置installed_app中的应用目录下加载task.py
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)