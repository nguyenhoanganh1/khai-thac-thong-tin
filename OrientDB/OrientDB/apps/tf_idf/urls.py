from django.http import request
from django.urls import path

from OrientDB.OrientDB.apps.tf_idf import views as tf_idf

urlpatterns = [
    path('tf-idf/manual', tf_idf.TFIDFManual(request), name='manual'),
    path('tf-idf/lib', tf_idf.TFIDFLib(request), name='lib'),
]
