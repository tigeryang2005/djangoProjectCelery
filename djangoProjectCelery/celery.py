import os
import django
from celery import Celery
from django.conf import settings

# 设置系统环境变量，安装django，必须设置，否则在启动celery时会报错
# djangoProjectCelery 是当前项目名
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectCelery.settings')
django.setup()
# 实例化一个
celery_app = Celery('djangoProjectCelery')
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)