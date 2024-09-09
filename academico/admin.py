from django.contrib import admin
from .models import *



admin.site.register(Parentezco)
    




@admin.register(Tutores)
class TutoresAdmin(admin.ModelAdmin):
    list_display = ('Apellido', 'Nombre', 'DNI')
    search_fields = ('apellidos', 'nombres', 'dni')
    list_filter = ('DNI',)


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('get_Tutores', 'Nombre_Familia')
    list_filter = ('Nombre_Familia',)

    def get_Tutores(self, obj):
        return ', '.join([tutores.Nombre for tutores in obj.Tutores.all()])
    get_Tutores.short_description = 'tutores'


@admin.register(Alumnos)
class AlumnosAdmin(admin.ModelAdmin):
    list_display = ('Apellidos', 'Nombres', 'DNI', 'Edad', 'Fecha_Nacimiento', 'Familia',)
    search_fields = ('apellidos', 'nombres', 'dni', 'fecha_nacimiento', 'familia', 'tutor')
    list_filter = ('Familia', 'Baja_Alumno', 'Casa', 'Colegio','Lugar_Nacimiento', 'Nacionalidad', 'Localidad', 'Sexo')

    # Puedes añadir más opciones a tu administrador aquí:
    #  -  ordering = ('apellidos',) # para ordenar por apellido 
    #  -  list_editable = ('Edad',) # para editar campos directamente en la lista
    #  -  readonly_fields = ('Fecha_Nacimiento',) # para hacer un campo solo de lectura

@admin.register(Valor)
class ValorAdmin(admin.ModelAdmin):
    list_display = ('Valor',)
    search_fields = ('Valor',)

@admin.register(Asistencias)
class AsistenciasAdmin(admin.ModelAdmin):
    list_display = ('Dia','Alumno','Valor',)
    search_fields = ('Alumno',)


@admin.register(Casas)
class CasasAdmin(admin.ModelAdmin):
    list_display = ('Nombre',)
    search_fields = ('Nombre',)

@admin.register(Colegios)
class ColegiosAdmin(admin.ModelAdmin):
    list_display = ('Nombre',)
    search_fields = ('Nombre',)

@admin.register(Lugar_Nacimiento)
class Lugar_NacimientoAdmin(admin.ModelAdmin):
    list_display = ('Lugar',)
    search_fields = ('Lugar',)

@admin.register(Nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ('Nacionalidad',)
    search_fields = ('Nacionalidad',)

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('Localidad',)
    search_fields = ('Localidad',)

@admin.register(Cuotas)
class CuotasAdmin(admin.ModelAdmin):
    list_display = ('Alumnos',  'Fecha_hora', 'Pagado',)
    search_fields = ('Alumnos__apellidos', 'Alumnos__nombres',  'Fecha_hora',)  # Buscar por campos relacionados
    list_filter = ( 'Pagado',) 

    # Puedes añadir más opciones a tu administrador aquí:
    #  -  ordering = ('Mes_año',) # para ordenar por mes y año
    #  -  list_editable = ('Pagado',) # para editar si está pagado directamente en la lista
    #  -  readonly_fields = ('Fecha_hora',) # para hacer la fecha y hora de creación solo de lectura


@admin.register(Cursos)
class CursosAdmin(admin.ModelAdmin):
    list_display = ( 'Division', 'get_materias',) 
    search_fields = ( 'Division__Division', 'Nivel__Nivel',) # Buscar por campos relacionados
    list_filter = ( 'Division',) 
    filter_horizontal = ('Materias',) # Usa filter_horizontal para la relación ManyToMany

    def get_materias(self, obj):
        return ", ".join([materia.Denominación for materia in obj.Materias.all()])
    get_materias.short_description = "Materias"









@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('Division',)
    search_fields = ('Division',)

@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('Nivel',)
    search_fields = ('Nivel',)





@admin.register(Nivel_Docente)
class Nivel_DocenteAdmin(admin.ModelAdmin):
    list_display = ('Nivel',)
    search_fields = ('Nivel',)

@admin.register(Titulos_Profesionales)
class Titulos_ProfesionalesAdmin(admin.ModelAdmin):
    list_display = ('Denominación', 'Observación')
    search_fields = ('Denominación', 'Observación')

@admin.register(Docentes)
class DocentesAdmin(admin.ModelAdmin):
    list_display = ('Nivel_Docente', 'Apellidos', 'Nombres', 'CUIL', 'Tel', 'F_Nacimiento', 'Titulo',)
    search_fields = ('Nivel_Docente', 'Apellidos', 'Nombres', 'CUIL', 'Tel', 'F_Nacimiento', 'Titulo')
    list_filter = ('Apellidos', 'Apellidos','CUIL',)


@admin.register(Materias)
class MateriasAdmin(admin.ModelAdmin):
    list_display = ('Denominación', 'Docente_Titular',)
    search_fields = ('Denominación', 'Docente_Titular',)
    list_filter = ('Docente_Titular', 'Denominación')


@admin.register(notas)
class notasAdmin(admin.ModelAdmin):
    list_display = ('alumnos', 'participacion_en_clases', 'tp_individual_1', 'tp_individual_2', 'leccion_oral_individual', 'evaluacion_escrita', 'exposicion_grupal_nota_grupal', 'exposicion_grupal_nota_individual', 'exposicion_grupal_soporte_presentacion', 'laboratorio_taller', 'carpeta', 'material', 'conducta')
    search_fields = ('alumnos__nombre', 'participacion_en_clases', 'tp_individual_1', 'tp_individual_2', 'leccion_oral_individual', 'evaluacion_escrita', 'exposicion_grupal_nota_grupal', 'exposicion_grupal_nota_individual', 'exposicion_grupal_soporte_presentacion', 'laboratorio_taller', 'carpeta', 'material', 'conducta')
    filter_horizontal = ('materias',)





























admin.site.site_header = 'Colegio Sagrado Corazón'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Administración del Colegio'