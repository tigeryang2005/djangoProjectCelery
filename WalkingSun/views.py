import json
import random
import threading

from celery import result

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse

from WalkingSun.tasks import add
import logging

logger = logging.getLogger('log')


# Create your views here.

def index(request):
    return render(request, 'index.html')


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
