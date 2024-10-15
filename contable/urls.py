from django.contrib import admin
from django.urls import path
from contable import views

urlpatterns = [
    path('conta', views.contable, name= "index_conta"),
]

        ## LISTA DE MATRICULAS
urlpatterns += [
    path('matriculas/', views.listar_matriculas, name='listar_matriculas'),
    path('matriculas/crear/', views.crear_matricula, name='crear_matricula'),
    path('sin_tutor/<int:alumno_id>/', views.sin_tutor, name='sin_tutor'),
]