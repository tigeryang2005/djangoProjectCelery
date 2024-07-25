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
from django.urls import path

from WalkingSun.views import CelerytestView, CeleryResultView, PhoneListView
from WalkingSun import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('celerytask/', CelerytestView.as_view(), name="celery_test_view"),
    path('celeryinfo/', CeleryResultView.as_view(), name="celery_result_view"),
    path('phone/list/', PhoneListView.as_view(), name="phone_list_view"),
    path('index/', views.index),
    path('login/', views.login),
    path('department/', views.department),
]
