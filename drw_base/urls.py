from django.urls import path
from . import views


urlpatterns = [
    #path('drw_base/', views.drw_list, name='drw_list'),
    path('',                   views.drw_list,          name='drw_list'          ),
    path('drw/<int:pk>/',      views.drw_detail,        name='drw_detail'        ),
    path('drw/new/',           views.drw_new,           name='drw_new'           ),
    path('drw/<int:pk>/edit/', views.drw_edit,          name='drw_edit'          ),
    path('drw/result/',        views.drw_search_result, name='drw_search_result' ),
    path('drw/szukaj/',        views.get_szuk_lanc,     name='get_szuk_lanc'     ),
    path('drw/pdf_view/<int:pk>/',      views.pdf_view,          name='pdf_view'          ),
]