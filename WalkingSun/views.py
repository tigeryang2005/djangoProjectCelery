import json
import random
import threading

from celery import result

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from WalkingSun.tasks import add
import logging

logger = logging.getLogger('log')


# Create your views here.

class CelerytestView(View):
    def get(self, request, *args, **kwargs):
        thread_receive_task = threading.Thread(target=self.receive_task, args=())
        thread_receive_task.start()
        return HttpResponse(f"你好,任务已收到")

    def receive_task(self):
        infos = []
        for i in range(1000):
            x, y = random.randint(0, 10), random.randint(0, 10)
            t = add.delay(x, y, queue="tasks", routing_key="tasks")
            t_id = t.task_id
            # task_ids.append(t_id)
            infos.append(f"task_id:{t_id},x:{x}, y:{y}")
        # res = json.dumps(task_ids)
        logger.info('---')
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
