from django.http import request
from django.urls import path

from OrientDB.OrientDB.apps.page_rank import views as page_rank

urlpatterns = [

    path('page-rank/manual', page_rank.pageRankLib(request), name='index'),
    path('page-rank/lib', page_rank.pageRankManual(request), name='index'),

]
