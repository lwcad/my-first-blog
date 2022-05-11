from django.urls import path
from . import views


urlpatterns = [
    #path('',                       views.drw_list,             name='drw_list'            ), # lista rysunków nie stronicowana - nie używana obecnie

    path('',                       views.get_szuk_lanc,        name='get_szuk_lanc'       ),
    path('drw/list',               views.drw_list_paginate,    name='drw_list_paginate'   ),
    path('drw/<int:pk>/',          views.drw_detail,           name='drw_detail'          ),
    path('drw/new/',               views.drw_new,              name='drw_new'             ),
    path('drw/<int:pk>/edit/',     views.drw_edit,             name='drw_edit'            ),
    path('drw/result/',            views.drw_search_result,    name='drw_search_result'   ),
    path('drw/pdf_view/<int:pk>/', views.pdf_view,             name='pdf_view'            ),
    path('drw/serwis/',            views.serwis,               name='serwis'              ),
    path('niezwerifik/',           views.drw_niezweryfik_list, name='drw_niezweryfik_list'),
    path('drw/<pk>/weryfikuj/',    views.drw_weryfikuj,        name='drw_weryfikuj'       ),
    path('drw/<pk>/remove/',       views.drw_remove,           name='drw_remove'          ),
    path('register/',              views.register_request,     name='register'            ),
    path('login/',                 views.login_request,        name='login'               ),
    path('logout/',                views.logout_request,       name= 'logout'),
]