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
        fields = '__all__'
        exclude = ('Fecha_Nacimiento',)  # Excluye el campo Fecha_Nacimiento




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



class CuotaForm(forms.ModelForm):
    class Meta:
        model = Cuotas
        fields = ['Alumnos', 'Mes_año', 'Fecha_hora', 'Pagado']
        widgets = {
            'Mes_año': forms.DateInput(attrs={'type': 'date'}),
            'Fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


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


class CursosForm(forms.ModelForm):
 

    class Meta:
        model = Cursos
        fields = ['años', 'Division', 'Materias', 'Nivels'] 

class NotasForm(forms.ModelForm):
    class Meta:
        model = notas
        fields = [
            'alumnos',
            'materias',
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
            'materias': forms.CheckboxSelectMultiple,
        }