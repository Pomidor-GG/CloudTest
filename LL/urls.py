from django.urls import path

from .views import *


urlpatterns = [
    path('', landing, name='landing_url'),
    path('ourworks/', works_list, name='list_of_works_url'),
    path('ourworks/<str:slug>/', work_detail, name='work_detail_url'),
]