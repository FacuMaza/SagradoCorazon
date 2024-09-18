from django.contrib import admin
from django.urls import path
from academico import views
from .views import AlumnosListView

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
    path('familia/<int:pk>/editar/', views.familia_update, name='familia_update'),
    path('familia/<int:pk>/detail/', views.familia_detail, name='familia_detail'),
    path('familia/<int:pk>/eliminar/', views.familia_delete, name='familia_delete'),
]



# CASAS, COLEGIOS , LUGAR DE NACIMIENTO , LOCALIDAD , NACIONALIDAD  
urlpatterns += [
    path('casas/', views.casa_list, name='casa_list'),
   
    path('casas/create/', views.casa_create, name='casa_create'),
  
    path('colegios/', views.colegio_list, name='colegio_list'),
    
    path('colegios/create/', views.colegio_create, name='colegio_create'),


    path('lugar_nacimiento/', views.lugar_nacimiento_list, name='lugar_nacimiento_list'),
   
    path('lugar_nacimiento/create/', views.lugar_nacimiento_create, name='lugar_nacimiento_create'),
    path('lugar_nacimiento/<int:pk>/update/', views.lugar_nacimiento_update, name='lugar_nacimiento_update'),
 

    path('nacionalidad/', views.nacionalidad_list, name='nacionalidad_list'),
 
    path('nacionalidad/create/', views.nacionalidad_create, name='nacionalidad_create'),
    path('nacionalidad/<int:pk>/update/', views.nacionalidad_update, name='nacionalidad_update'),
  

    path('localidad/', views.localidad_list, name='localidad_list'),

    path('localidad/create/', views.localidad_create, name='localidad_create'),
    path('localidad/<int:pk>/update/', views.localidad_update, name='localidad_update'),

]



                                        #ALUMNOS

urlpatterns += [
    path('lista_alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alumnos/<int:pk>/', views.detalle_alumno, name='detalle_alumno'),
    path('nuevo/', views.nuevo_alumno, name='nuevo_alumno'),
    path('alumnos/<int:pk>/editar/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/<int:pk>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
]


                        ##ASISTENCIAS

urlpatterns += [
    path('asistencia/', views.asistencias_list, name='asistencias_list'),
    path('asistencia/add/', views.asistencia_add, name='asistencia_add'),
    path('asistencia/<int:pk>/edit/', views.asistencia_edit, name='asistencia_edit'),
    
]

                            ##VALOR

urlpatterns += [
    path('valor/', views.listar_valores, name='listar_valores'),
    path('valor/crear/', views.crear_valor, name='crear_valor'),
    path('valoreditar/<int:valor_id>/', views.editar_valor, name='editar_valor'),
]

                    ##CUOTAS


urlpatterns += [
    path('cuotas/', views.cuotas_list, name='cuotas_list'),
    path('cuotas/<int:pk>/', views.cuota_detail, name='cuota_detail'),
    path('cuotas/create/', views.cuota_create, name='cuota_create'),
    path('cuotas/<int:pk>/update/', views.cuota_update, name='cuota_update'),
    path('cuotas/<int:pk>/delete/', views.cuota_delete, name='cuota_delete'),
]


urlpatterns += [

    path('division/', views.list_division, name='list_division'),
    path('division/crear/', views.crear_division, name='crear_division'),


    path('nivel/', views.list_nivel, name='list_nivel'),
    path('nivel/crear/', views.crear_nivel, name='crear_nivel'),


    path('nivel_docente/', views.list_nivel_docente, name='list_nivel_docente'),
    path('nivel_docente/crear/', views.crear_nivel_docente, name='crear_nivel_docente'),


    path('titulo_profesional/', views.list_titulos_profesionales, name='list_titulos_profesionales'),
    path('titulo_profesional/crear/', views.crear_titulo_profesional, name='crear_titulo_profesional'),
]



#DOCENTES

urlpatterns += [
    path('docentes/', views.docentes_list, name='docentes_list'),
    path('docentes/<int:pk>/', views.docente_detail, name='docente_detail'),
    path('docentes/create/', views.docente_create, name='docente_create'),
    path('docentes/<int:pk>/update/', views.docente_update, name='docente_update'),
    path('docentes/<int:pk>/delete/', views.docente_delete, name='docente_delete'),
]

#MATERIAS
urlpatterns += [
    path('materia/', views.materia_list, name='materia_list'),
    path('materia/<int:pk>/', views.materia_detail, name='materia_detail'),
    path('materia/create/', views.materia_create, name='materia_create'),
    path('materia/<int:pk>/update/', views.materia_update, name='materia_update'),
    path('materia/<int:pk>/delete/', views.materia_delete, name='materia_delete'),
]

#CURSOS

urlpatterns += [
    path('cursos/', views.cursos_list, name='cursos_list'),
    path('cursos/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('cursos/create/', views.curso_create, name='curso_create'),
    path('cursos/<int:curso_id>/update/', views.curso_update, name='curso_update'),
    path('cursos/<int:curso_id>/delete/', views.curso_delete, name='curso_delete'),
]



#AGREGAR MATERIAS EN CURSOS
urlpatterns += [
     path('materias_curso/<int:curso_id>/', views.materias_curso, name='materias_curso'),
]

#AGREGAR ALUMNOS EN CURSOS
urlpatterns += [
   
    path('cursos/<int:curso_id>/agregar_alumno/', views.agregar_alumno_curso, name='agregar_alumno_curso'),
    path('materia/<int:curso_id>/alumnos/', AlumnosListView.as_view(), name='alumnos_por_materia'),
    path('curso/<int:curso_id>/alumnos/', AlumnosListView.as_view(), name='alumnos_list'),
]
