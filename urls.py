from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [


    path('bitrix_1c/', views.bitrix_1c, name='bitrix_1c'),
    path('teh_1c/', views.teh_1c, name='teh_1c'),
    path('tv_1c/', views.tv_1c, name='tv_1c'),
    path('tg_sms/', views.tg_sms, name='tg_sms'),
    path('date_tehpod/', views.date_tehpod, name='date_tehpod'),


]

