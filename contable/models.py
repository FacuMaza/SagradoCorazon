from django.utils import timezone
from django.db import models
from academico.models import *
 

class Matricula(models.Model):
    alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    
    años = [('2018', '2018'),('2019', '2019'),('2020', '2020'),('2021', '2021'),('2022', '2022'),('2023', '2023'),('2024', '2024'),('2025', '2025'),('2026', '2026'),('2027', '2027'),('2028', '2028'),('2029', '2029'),]
    Año = models.CharField(max_length=4, choices=años)
    monto_matricula = models.FloatField()
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s '%(self.alumno, self.Año)
    class Meta:
        db_table = 'matriculas'
        verbose_name = 'matricula'
        verbose_name_plural = 'matriculas'

class pagomatricula(models.Model):
    matriculas = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    efectivo = models.FloatField(null=True, blank=True)
    transferencia = models.FloatField(null=True, blank=True)
    cheque = models.FloatField(null=True, blank=True)
    pagare = models.FloatField(null=True, blank=True)
    fecha_pago_matricula = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s %s %s %s %s'%(self.matriculas, self.efectivo , self.transferencia , self.cheque , self.pagare)

    class Meta:
        db_table = 'pagomatriculas'
        verbose_name = 'pagomatricula'
        verbose_name_plural = 'pagomatriculas'


class pagocuota(models.Model):
    cuota = models.ForeignKey(Cuotas, on_delete=models.CASCADE)
    efectivo = models.FloatField(null=True, blank=True)
    transferencia = models.FloatField(null=True, blank=True)
    cheque = models.FloatField(null=True, blank=True)
    pagare = models.FloatField(null=True, blank=True)
    descuento = models.FloatField(default=0,null=True, blank=True)

    def __str__(self):
        return '%s '%(self.cuota, self.efectivo , self.transferencia , self.cheque , self.pagare)

    class Meta:
        db_table = 'pagocuotas'
        verbose_name = 'pagocuota'
        verbose_name_plural = 'pagocuotas'
