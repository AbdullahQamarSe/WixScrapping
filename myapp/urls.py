from django.urls import path,  include
from . import views


urlpatterns = [
path('', views.main_page, name='base'),
path('fashionphile/', views.home, name='home'),
path('ebay/', views.ebay, name='ebay'),
path('realreal/', views.realreal, name='realreal'),
path('maisondeluxe/', views.maisondeluxe, name='maisondeluxe'),
path('madison/', views.madison, name='madison'),
path('rebag/', views.rebag, name='rebag'),
path('firstdibs/', views.firstdibs, name='firstdibs'),
]