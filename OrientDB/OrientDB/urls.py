"""
URL configuration for OrientDB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.http import request
from django.urls import path

from OrientDB.OrientDB.apps.tf_idf import views as tf_idf
from OrientDB.OrientDB.apps.page_rank import views as page_rank

urlpatterns = [

    path('page-rank/manual', page_rank.pageRankLib(request), name='manual'),
    path('page-rank/lib', page_rank.pageRankManual(request), name='lib'),

    path('tf-idf/manual', tf_idf.TFIDFManual(request), name='manual'),
    path('tf-idf/lib', tf_idf.TFIDFLib(request), name='lib'),
]
