from django.urls import path
from . import views


urlpatterns = [
    #path('drw_base/', views.drw_list, name='drw_list'),
    path('', views.drw_list, name='drw_list'),
    path('drw/<int:pk>/', views.drw_detail, name='drw_detail'),
]