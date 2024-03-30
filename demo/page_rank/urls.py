from django.urls import path

from . import views

urlpatterns = [
    path('manual/', views.manual),
    path('crawl-data/', views.crawl_data),
    path('lib/', views.lib),
    path('website-list/', views.website_list, name='website_list'),
    path('create-website/', views.create_website, name='create_website'),

]