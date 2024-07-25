import logging
import random
import threading

from celery import result
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from WalkingSun import models
from WalkingSun.tasks import add

logger = logging.getLogger('log')


# Create your views here.
@transaction.atomic
def department_add(request):
    if request.method == 'GET':
        return render(request, 'department_add.html')
    if request.method == 'POST':
        logger.info(request.POST)
        title = request.POST.get('title', '')
        count = request.POST.get('count', 0)
        new_department = models.Department.objects.create(title=title, count=count)
        logger.info(model_to_dict(new_department))
        return redirect('/department/')


def department(request):
    # models.Department.objects.create(title="销售部", count=10)
    # models.Department.objects.create(**{"title": "服务部", "count": 11})

    # departments = models.Department.objects.all()
    # departments = models.Department.objects.filter(id__gt=1)
    departments = models.Department.objects.all().order_by('-id')
    for department in departments:
        print(department.id, department.title, department.count)
        department_dict = model_to_dict(department)
        print(department_dict)
        print(department_dict.get('name', '无'))

    # department = models.Department.objects.filter(id=1).first()
    # print(department.id, department.title, department.count)
    # department = models.Department.objects.get(id=2)
    # print(department.id, department.title, department.count)
    #
    # models.Department.objects.filter(id=1).delete()
    #
    # models.Department.objects.filter(id=2).update(count=99)
    return render(request, 'department.html', {'departments': departments})


def index(request):
    phone_list = [
        {"id": 1, "phone": "188888888888", "city": "上海1"},
        {"id": 2, "phone": "188888888887", "city": "上海2"},
        {"id": 3, "phone": "188888888886", "city": "上海3"},
        {"id": 3, "phone": "188888888885", "city": "上海3"},
    ]
    return render(request, 'index.html', {"phone_list": phone_list})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        if request.POST.get('user_name', '') == 'admin' and request.POST.get('password', '') == '123':
            logger.info(request.POST)
            return redirect('/index/')
        else:
            return render(request, 'login.html', {"error": "用户名或密码不正确"})


class PhoneListView(View):
    def get(self, request):
        phone_list = [
            {"id": 1, "phone": "188888888888", "city": "上海1"},
            {"id": 2, "phone": "188888888887", "city": "上海2"},
            {"id": 3, "phone": "188888888886", "city": "上海3"},
            {"id": 3, "phone": "188888888885", "city": "上海3"},
        ]
        return render(request, "phone_list.html", {"data": phone_list})


class CelerytestView(View):
    def get(self, request, *args, **kwargs):
        thread_receive_task = threading.Thread(target=self.receive_task, args=())
        thread_receive_task.start()
        return HttpResponse(f"你好,任务已收到")

    def receive_task(self):
        infos = []
        for i in range(10):
            x, y = random.randint(0, 10), random.randint(0, 10)
            # logger.info(i)
            t = add.apply_async([x, y], retries=5)
            # logger.info('finish')
            # add.delay(x, y)
            # infos.append(f"x:{x}, y:{y}")
            # t = add.delay(x, y)
            t_id = t.task_id
            # task_ids.append(t_id)
            infos.append(f"task_id:{t_id},x:{x}, y:{y}")
        # res = json.dumps(task_ids)
        # logger.info('---')
        logger.info(infos)


class CeleryResultView(View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id')
        # 异步执行
        ar = result.AsyncResult(task_id)

        if ar.ready():
            # print(ar.ready())
            return JsonResponse({'status': ar.state, 'result': ar.get(),
                                 })
        else:
            # print(ar.ready())
            return JsonResponse({'status': ar.state, 'result': ''})
