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
        fields = ['Nombre_Familia', 'Tutores']
        widgets = {
            'Tutores': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }



class AlumnosForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = '__all__'


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