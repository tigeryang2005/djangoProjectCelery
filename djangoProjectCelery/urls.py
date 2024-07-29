"""
URL configuration for djangoProjectCelery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path

from WalkingSun import views
from WalkingSun.views import CelerytestView, CeleryResultView, PhoneListView, DepartmentDeleteView

urlpatterns = [
    path('user/list/', views.UserListView.as_view(), name='user_list'),
    path('admin/', admin.site.urls),
    path('celerytask/', CelerytestView.as_view(), name="celery_test_view"),
    path('celeryinfo/', CeleryResultView.as_view(), name="celery_result_view"),
    path('phone/list/', PhoneListView.as_view(), name="phone_list_view"),
    path('index/', views.index),
    path('accounts/login/', views.login_custom, name='login'),
    path('department/', views.department, name='department_list'),
    path('department/add/', views.department_add),
    path('favicon.ico', serve, {'path': 'images/favicon.ico'}),
    path('department/list/', views.DepartmentListView.as_view(), name='department_list1'),
    path('department/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('department/add1/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('department/update/<int:pk>/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('department/delete/<int:pk>', DepartmentDeleteView.as_view(), name='department_delete'),
]
