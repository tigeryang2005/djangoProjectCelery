import logging
import random
import threading

from celery import result
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from WalkingSun import models
from WalkingSun.models import Department, UserProfile
from WalkingSun.tasks import add

logger = logging.getLogger('log')


# Create your views here.

class UserListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'user_list.html'
    context_object_name = 'user_list'
    ordering = ['-id']

    def get(self, request, *args, **kwargs):
        logger.info(request)
        response = super().get(request, *args, **kwargs)
        user_list = self.get_queryset()
        logger.info(serializers.serialize('json', user_list))
        return response


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'department_list.html'
    context_object_name = 'departments'
    ordering = ['-id']

    def get(self, request, *args, **kwargs):
        logger.info(request)
        response = super().get(request, *args, **kwargs)
        departments = self.get_queryset()
        logger.info(serializers.serialize('json', departments))
        return response


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'department_detail.html'
    context_object_name = 'department'

    def get(self, request, *args, **kwargs):
        logger.info(request)
        response = super().get(request, *args, **kwargs)
        logger.info(serializers.serialize('json', [self.get_object()]))
        return response


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    fields = ['title', 'count']
    template_name = 'department_edit.html'
    success_url = reverse_lazy('department_list1')

    def form_valid(self, form):
        # form.instance.created_by = self.request.user
        # form.instance.updated_by = self.request.user
        logger.info(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "新增部门"
        context['form_text'] = "新增"
        return context


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    fields = ['title', 'count']
    template_name = 'department_edit.html'
    success_url = reverse_lazy('department_list1')

    def form_valid(self, form):
        # form.instance.update_by = self.request.user
        logger.info(form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = "编辑部门"
        context['form_text'] = "保存"
        return context


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'department_delete.html'
    success_url = reverse_lazy("department_list1")

    def post(self, request, *args, **kwargs):
        logger.info(request)
        department_dict = model_to_dict(self.get_object())
        response = super().post(request, *args, **kwargs)
        logger.info(f"已删除的department: {department_dict}")
        return response


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
    # for department in departments:
    #     department_dict = model_to_dict(department)
    #     logger.info(department_dict)

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

    user_info = request.session.get("user_info", "")
    if not user_info:
        return redirect('login')
    return render(request, 'index.html', {"phone_list": phone_list, "user_info": user_info})


def login_custom(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        logger.info(request.POST)
        user = authenticate(username=request.POST.get('user_name'), password=request.POST.get('password'))
        if user:
            login(request, user)
            # """
            #     1.生成随机字符串
            #     2.返回用户浏览器的cookie中
            #     3.存储到网站的session中， 随机字符串+用户标识
            # """
            # request.session["user_info"] = {
            #     "last_name": user.last_name,
            #     "name": user.username,
            #     "id": user.id
            # }
            return redirect('department_list1')
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
