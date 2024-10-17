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
    path('imprimir_datos_padre_madre/<int:matricula_id>/', views.imprimir_datos_padre_madre, name='imprimir_datos_padre_madre'),

]

            ##lista de cuotas
urlpatterns += [
    path('cuota/', views.lista_cuotas, name='lista_cuotas'),
    path('cuota/<int:cuota_id>/', views.detalle_cuota, name='detalle_cuota'),
    path('cuotas_alumno/<int:alumno_id>/', views.cuotas_alumno, name='cuotas_alumno'),
    path('cuotas_alumno/<int:alumno_id>/pago_guardado/', views.cuotas_alumno_con_pago_guardado, name='cuotas_alumno_con_pago_guardado'),

    # path('cuota/crear/', views.crear_cuota, name='crear_cuota'),
    path('cuota/<int:cuota_id>/editar/', views.editar_cuota, name='editar_cuota'),
    
]

##PAGO DE CUOTAS    
urlpatterns += [
   path('pagar/<int:cuota_id>/', views.pagocuota_form, name='pagocuota_form'),
    path('cuota/<int:cuota_id>/detalle_pago/', views.detalle_pago, name='detalle_pago'),
]

##actualizacion de cuota
urlpatterns += [
   path('actualizar_cuotas/', views.actualizar_cuotas, name='actualizar_cuotas'),
]




