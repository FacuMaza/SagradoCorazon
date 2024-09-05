from django.contrib import admin
from django.urls import path
from academico import views

urlpatterns = [
    path('', views.index, name= "index"),
]

##URLS DE TUTORES

urlpatterns += [
    path('tutores_list/', views.tutores_list, name='tutores_list'),
    path('tutores/crear/', views.tutores_create, name='tutores_create'),
    path('tutores/<int:pk>/editar/', views.tutores_update, name='tutores_update'),
    path('tutores/<int:pk>/eliminar/', views.tutores_delete, name='tutores_delete'),
    path('tutores/<int:pk>/', views.tutores_detail, name='tutores_detail'),
]


##CONFIGURACION
urlpatterns += [
path('configuracion/', views.configuracion, name= "configuracion"),
]


# PARENTEZCO
urlpatterns += [
    path('parentezcos/', views.parentezcos_list, name='parentezcos_list'),
    path('parentezcos/crear/', views.parentezcos_create, name='parentezcos_create'),
    path('parentezcos/<int:pk>/editar/', views.parentezcos_update, name='parentezcos_update'),
    path('parentezcos/<int:pk>/eliminar/', views.parentezcos_delete, name='parentezcos_delete'),
]


#FAMILIAS

urlpatterns += [
    path('familia_list', views.familia_list, name='familia_list'),
    path('crear/', views.familia_create, name='familia_create'),
    path('<int:pk>/editar/', views.familia_update, name='familia_update'),
    path('<int:pk>/detail/', views.familia_detail, name='familia_detail'),
    path('<int:pk>/eliminar/', views.familia_delete, name='familia_delete'),
]