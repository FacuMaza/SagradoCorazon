from django import forms
from .models import *

class TutorForm(forms.ModelForm):
    
    class Meta:
        model = Tutores
        fields = '__all__'


class ParentezcoForm(forms.ModelForm):
    class Meta:
        model = Parentezco
        fields = '__all__'

class FamiliaForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ['Nombre_Familia']
        widgets = {
            'Nombre_Familia': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nombre_Familia'].required = False
       



class AlumnosForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = [
            'Familia',
            'Baja_Alumno',
            'Casa',
            'Domicilio',
            'curso',
            'Colegio',
            'Lugar_Nacimiento',
            'Nacionalidad',
            'Localidad',
            'Apellidos',
            'Nombres',
            'DNI',
            'Edad',
            'Fecha_Nacimiento',
            'Email_Institucional',
            'Email_Personal',
            'Escuela_Procedencia',
            'Enfermedades',
            'Toma_Medicamentos',
            'Telefono_Urgencia',
            'Sexo',
            # ... Otros campos del modelo Alumnos (sin 'curso')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener todos los cursos ordenados por el campo "curso"
        cursos = Cursos.objects.all().order_by('años', 'Division')
        choices = [(curso.id, f"{curso.años.Año} - {curso.Division}") for curso in cursos]
        self.fields['curso'].widget = forms.Select(choices=choices)
        



class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencias
        fields = ['Dia', 'Alumno', 'Valor']
        widgets = {
            'Dia': forms.DateInput(attrs={'type': 'date'}),
        }

class ValorForm(forms.ModelForm):
    class Meta:
        model = Valor
        fields = ['Valor']



# class CuotaForm(forms.ModelForm):
#     class Meta:
#         model = Cuotas
#         fields = ['Alumnos', 'Mes_año', 'Fecha_hora', 'Pagado']
#         widgets = {
#             'Mes_año': forms.DateInput(attrs={'type': 'date'}),
#             'Fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = '__all__'

class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = '__all__'

class NivelDocenteForm(forms.ModelForm):
    class Meta:
        model = Nivel_Docente
        fields = '__all__'

class TitulosProfesionalesForm(forms.ModelForm):
    class Meta:
        model = Titulos_Profesionales
        fields = '__all__'


class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docentes
        fields = ['Nivel_Docente', 'Apellidos', 'Nombres', 'CUIL', 'Tel', 'Titulo'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Nivel_Docente'].queryset = Nivel_Docente.objects.all()
        self.fields['Titulo'].queryset = Titulos_Profesionales.objects.all()

        # Si el formulario es para crear un nuevo docente, incluimos el campo F_Nacimiento
        if self.instance.pk is None:
            self.fields['F_Nacimiento'] = forms.DateField(label='Fecha de Nacimiento', required=True)


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materias
        fields = ['Docente_Titular', 'Denominación',]



class NivelForm(forms.ModelForm):
    class Meta:
        model = Nivel
        fields = '__all__'

class AñosForm(forms.ModelForm):
    class Meta:
        model = Años
        fields = '__all__'



class CursosForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        año = cleaned_data.get('años')  # Ensure correct field name
        division = cleaned_data.get('Division')  # Ensure correct field name

        # Verifica si ya existe un curso con la misma combinación
        existing_curso = Cursos.objects.filter(años=año, Division=division).exists()

        if existing_curso:
            raise forms.ValidationError("Ya existe un curso con este año y división.")
        return cleaned_data

    class Meta:
        model = Cursos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener todos los años y niveles
        años = Años.objects.all()
        niveles = Nivel.objects.all()

        # Prepara las opciones para el campo 'años' en el formulario
        año_choices = [(año.id, str(año)) for año in años]
        self.fields['años'].widget = forms.Select(choices=año_choices)

        # Prepara las opciones para el campo 'Nivels' en el formulario
        nivel_choices = [(nivel.id, str(nivel)) for nivel in niveles]
        self.fields['Nivels'].widget = forms.Select(choices=nivel_choices)

class NotasForm(forms.ModelForm):
    class Meta:
        model = notas
        fields = [
            'participacion_en_clases',
            'tp_individual_1',
            'tp_individual_2',
            'leccion_oral_individual',
            'evaluacion_escrita',
            'exposicion_grupal_nota_grupal',
            'exposicion_grupal_nota_individual',
            'exposicion_grupal_soporte_presentacion',
            'laboratorio_taller',
            'carpeta',
            'material',
            'conducta',
        ]
        widgets = {
            'participacion_en_clases': forms.TextInput,
            'tp_individual_1': forms.TextInput,
            'tp_individual_2': forms.TextInput,
            'leccion_oral_individual': forms.TextInput,
            'evaluacion_escrita': forms.TextInput,
            'exposicion_grupal_nota_grupal': forms.TextInput,
            'exposicion_grupal_nota_individual': forms.TextInput,
            'exposicion_grupal_soporte_presentacion': forms.TextInput,
            'laboratorio_taller': forms.TextInput,
            'carpeta': forms.TextInput,
            'material': forms.TextInput,
            'conducta': forms.TextInput,
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].required = False