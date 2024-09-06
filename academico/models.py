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




class Alumnos(models.Model):
    Familia = models.ForeignKey(Familia, on_delete=models.CASCADE)
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


class Cuotas(models.Model):
    Alumnos = models.ForeignKey(Alumnos, on_delete=models.CASCADE)
    Mes_año = models.DateField(default=None)
    Fecha_hora = models.DateTimeField()
    Pagado = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s '%(self.Alumnos)

    class Meta:
        db_table = 'Cuotas'
        verbose_name = 'Cuota'
        verbose_name_plural = 'Cuotas'



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


class Cursos(models.Model):
    año = [('1', 'Primero'),('2', 'Segundo'),('3', 'Tercero'),('4', 'Cuarto'),('5', 'Quinto'),('6', 'Sexto'),('7', 'Septimo'),]
    años = models.CharField(max_length=1, choices=año, default=1)
    Division = models.ForeignKey(Division, on_delete=models.CASCADE)
    Materias = models.ManyToManyField(Materias,blank=False)
    nivel = [('1', 'Inicial'),('2', 'Primario'),('3', 'Secundario')]
    Nivels = models.CharField(max_length=1, choices=nivel, default=1)

    def __str__(self):
        return ' %s '%(self.Año)

    class Meta:
        db_table = 'Cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'