from django.contrib import admin
from .models import *

@admin.register(Matricula)
class matricula(admin.ModelAdmin):
    list_display = ('alumno', 'Año', 'monto_matricula','pagado')
    search_fields = ('alumno', 'Año', 'monto_matricula','pagado')
    list_filter = ('alumno',)

@admin.register(pagomatricula)
class pagomatricula(admin.ModelAdmin):
    list_display = ('matriculas', 'efectivo', 'transferencia','cheque','pagare','fecha_pago_matricula')
    search_fields = ('matriculas', 'efectivo', 'transferencia','cheque','pagare','fecha_pago_matricula')
    list_filter = ('matriculas',)


@admin.register(pagocuota)
class pagocuota(admin.ModelAdmin):
    list_display = ('cuota', 'efectivo', 'transferencia','cheque','pagare')
    search_fields = ('cuota', 'efectivo', 'transferencia','cheque','pagare')
    list_filter = ('cuota',)