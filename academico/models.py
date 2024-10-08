from datetime import date
from django.db import models




class Parentezco(models.Model):
    parentezco = models.CharField(max_length=255)

    def __str__(self):
        return '%s '%(self.parentezco)

    class Meta:
        db_table = 'Parentezcos'
        verbose_name = 'Parentezco'
        verbose_name_plural = 'Parentezcos'


class Tutores(models.Model):
    Nombre = models.CharField(max_length=255)
    Apellido = models.CharField(max_length=255)
    DNI = models.CharField(max_length=255)
    Domicilio_Personal = models.CharField(max_length=255)
    Domicilio_Laboral = models.CharField(max_length=255)
    Celular = models.CharField(max_length=255)
    Ocupacion = models.CharField(max_length=255)
    Email = models.EmailField()
    vive = [('S', 'Si'),('N', 'No'),]
    Vive = models.CharField(max_length=1, choices=vive)
    Responsable_de_pago = models.BooleanField()
    Parentezco = models.ForeignKey(Parentezco, on_delete=models.CASCADE)
    asignado = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s '%(self.Nombre,self.Apellido)

    class Meta:
        db_table = 'tutores'
        verbose_name = 'tutor'
        verbose_name_plural = 'tutores'

class Familia(models.Model):
    Tutores = models.ManyToManyField(Tutores,blank=False)
    Nombre_Familia = models.CharField(max_length=255, default=None)

    def __str__(self):
        return '%s '%(self.Nombre_Familia)

    class Meta:
        db_table = 'familias'
        verbose_name = 'familia'
        verbose_name_plural = 'familias'


class Casas(models.Model):
    Nombre = models.CharField(max_length=30)

    def __str__(self):
        return '%s '%(self.Nombre)

    class Meta:
        db_table = 'Casas'
        verbose_name = 'Casa'
        verbose_name_plural = 'Casas'

class Colegios(models.Model):
    Nombre = models.CharField(max_length=30)

    def __str__(self):
        return '%s '%(self.Nombre)

    class Meta:
        db_table = 'Colegios'
        verbose_name = 'Colegio'
        verbose_name_plural = 'Colegios'

class Lugar_Nacimiento(models.Model):
    Lugar = models.CharField(max_length=30)

    def __str__(self):
        return '%s '%(self.Lugar)

    class Meta:
        db_table = 'Lugar de Nacimiento'
        verbose_name = 'Lugar de Nacimiento'
        verbose_name_plural = 'Lugar de Nacimientos'


class Nacionalidad(models.Model):
    Nacionalidad = models.CharField(max_length=30)

    def __str__(self):
        return '%s '%(self.Nacionalidad)

    class Meta:
        db_table = 'Nacionalidades'
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'


class Localidad(models.Model):
    Localidad = models.CharField(max_length=30)

    def __str__(self):
        return '%s '%(self.Localidad)

    class Meta:
        db_table = 'Localidades'
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'


class Nivel_Docente(models.Model):
    Nivel = models.CharField(max_length=255)

    def __str__(self):
        return ' %s '%(self.Nivel)

    class Meta:
        db_table = 'Nivel de Docentes'
        verbose_name = 'Nivel de Docente'
        verbose_name_plural = 'Nivel de Docentes'

class Titulos_Profesionales(models.Model):
    Denominación = models.CharField(max_length=255)
    Observación = models.TextField()

    def __str__(self):
        return ' %s '%(self.Denominación)

    class Meta:
        db_table = 'Titulos Profesionales'
        verbose_name = 'Titulos Profesional'
        verbose_name_plural = 'Titulos Profesionales'

class Docentes(models.Model):
    Nivel_Docente = models.ForeignKey(Nivel_Docente, on_delete=models.CASCADE)
    Apellidos = models.CharField(max_length=255)
    Nombres = models.CharField(max_length=255)
    CUIL = models.CharField(max_length=255)
    Tel = models.CharField(max_length=255)
    F_Nacimiento = models.DateField()
    Titulo = models.ForeignKey(Titulos_Profesionales, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s '%(self.Apellidos, self.Nombres)

    class Meta:
        db_table = 'Docentes'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'



class Materias(models.Model):
    Denominación = models.CharField(max_length=255)
    Docente_Titular = models.ForeignKey(Docentes, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s '%(self.Denominación, self.Docente_Titular)

    class Meta:
        db_table = 'Materias'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
    

class Division(models.Model):
    Division = models.CharField(max_length=255)
    def __str__(self):
        return '%s '%(self.Division)

    class Meta:
        db_table = 'Divisiones'
        verbose_name = 'Division'
        verbose_name_plural = 'Divisiones'


class Nivel(models.Model):
    Nivel = models.CharField(max_length=255)

    def __str__(self):
        return '%s '%(self.Nivel)

    class Meta:
        db_table = 'Niveles'
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'


class Cursos(models.Model):
    año = [('1', 'Primero'),('2', 'Segundo'),('3', 'Tercero'),('4', 'Cuarto'),('5', 'Quinto'),('6', 'Sexto'),('7', 'Septimo'),]
    años = models.CharField(max_length=1, choices=año, default=1)
    Division = models.ForeignKey(Division, on_delete=models.CASCADE)
    Materias = models.ManyToManyField(Materias,blank=False, related_name="cursos")
    nivel = [('1', 'Inicial'),('2', 'Primario'),('3', 'Secundario')]
    Nivels = models.CharField(max_length=1, choices=nivel, default=1)

    def __str__(self):
        return '%s - %s %s'%(self.id, self.años, self.Division)

    class Meta:
        db_table = 'Cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Alumnos(models.Model):
    Familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, null=True, blank=True)
    Baja_Alumno = models.BooleanField()
    Casa = models.ForeignKey(Casas, on_delete=models.CASCADE)
    Colegio = models.ForeignKey(Colegios, on_delete=models.CASCADE)
    Lugar_Nacimiento = models.ForeignKey(Lugar_Nacimiento, on_delete=models.CASCADE)
    Nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    Localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    Apellidos = models.CharField(max_length=255)
    Nombres = models.CharField(max_length=255)
    DNI = models.CharField(max_length=255)
    Edad = models.IntegerField()
    Fecha_Nacimiento = models.DateField()
    Domicilio = models.CharField(max_length=255)
    Email_Institucional = models.EmailField()
    Email_Personal = models.EmailField()
    Escuela_Procedencia = models.CharField(max_length=255)
    Enfermedades = models.CharField(max_length=255)
    Toma_Medicamentos = models.CharField(max_length=255)
    Telefono_Urgencia = models.CharField(max_length=255)
    generos = [('V', 'Varón'),('M', 'Mujer'),]
    Sexo = models.CharField(max_length=1, choices=generos)

    def __str__(self):
        return '%s %s '%(self.Apellidos, self.Nombres)
    
    def save(self, *args, **kwargs):
        # Calculate age when saving
        if self.Fecha_Nacimiento:
            today = date.today()
            age = today.year - self.Fecha_Nacimiento.year - ((today.month, today.day) < (self.Fecha_Nacimiento.month, self.Fecha_Nacimiento.day))
            self.Edad = age
        super(Alumnos, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Alumnos'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'


class Valor(models.Model):
    Valor = models.CharField(max_length=255)

    def __str__(self):
        return '%s  '%(self.Valor)

    class Meta:
        db_table = 'Valores'
        verbose_name = 'Valor'
        verbose_name_plural = 'Valores'

class Asistencias(models.Model):
    Dia = models.DateField()
    Alumno = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    Valor = models.ForeignKey(Valor, on_delete=models.CASCADE)

    def __str__(self):
        return '%s  '%(self.Alumno)

    class Meta:
        db_table = 'Asistencias'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

class mes_año(models.Model):
    codigo_mes = models.IntegerField(default=None)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s '%(self.codigo_mes, self.descripcion)

    class Meta:
        db_table = 'mes_años'
        verbose_name = 'mes_año'
        verbose_name_plural = 'mes_años'


class Cuotas(models.Model):
    Alumnos = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    Tutor = models.ForeignKey(Tutores, on_delete=models.CASCADE,default=None)
    Mes_año = models.ForeignKey(mes_año, on_delete=models.CASCADE) ## MES Y AÑO QUE SE ABONA LA CUOTA
    Fecha_hora_del_pago = models.DateField(default=None) ## FECHA Y HORA DEL PAGO DE LA CUOTA
    Monto_cuota = models.FloatField(default=200000)
    Pagado = models.BooleanField(default=False)
    Anticipado = models.BooleanField(default=False)
    Anticipado_pagado = models.BooleanField(default=False)
    Extraordinario = models.CharField(max_length=255, default=None, blank=True)

    def __str__(self):
        return '%s %s '%(self.Alumnos, self.Mes_año)

    class Meta:
        db_table = 'Cuotas'
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'



class notas(models.Model):
    alumno = models.ForeignKey(Alumnos,  default=1, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materias, default=1, on_delete=models.CASCADE)
    participacion_en_clases = models.CharField(max_length=255,blank=True, null=True)
    tp_individual_1 = models.CharField(max_length=255,blank=True, null=True)
    tp_individual_2 = models.CharField(max_length=255,blank=True, null=True)
    leccion_oral_individual = models.CharField(max_length=255,blank=True, null=True)
    evaluacion_escrita = models.CharField(max_length=255,blank=True, null=True)
    exposicion_grupal_nota_grupal = models.CharField(max_length=255,blank=True, null=True)
    exposicion_grupal_nota_individual = models.CharField(max_length=255,blank=True, null=True)
    exposicion_grupal_soporte_presentacion = models.CharField(max_length=255,blank=True, null=True)
    laboratorio_taller = models.CharField(max_length=255,blank=True, null=True)
    carpeta = models.CharField(max_length=255,blank=True, null=True)
    material = models.CharField(max_length=255,blank=True, null=True)
    conducta = models.CharField(max_length=255,blank=True, null=True)

    class Meta:
        db_table = 'notas'
        verbose_name = 'nota'
        verbose_name_plural = 'notas'

