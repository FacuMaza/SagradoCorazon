from django import forms
from .models import *


class MatriculaForm(forms.ModelForm):
    Familia = forms.ModelChoiceField(queryset=Familia.objects.all(), label="Familia", widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione una familia")
    alumno = forms.ModelChoiceField(queryset=Alumnos.objects.all(), label="Alumno", widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Seleccione un alumno")

    class Meta:
        model = Matricula
        fields = ['Familia', 'alumno', 'Año', 'monto_matricula']
        widgets = {
            'Año': forms.Select(attrs={'class': 'form-control'}),
            'monto_matricula': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inicializar ambos campos como vacíos
        self.fields['Familia'].empty_label = "Seleccione una familia"
        self.fields['alumno'].empty_label = "Seleccione un alumno"

        # Manejar la actualización de alumnos cuando se selecciona una familia
        if self.is_bound:
            # Obtener la familia seleccionada
            familia_id = self.data.get('Familia')
            if familia_id:
                # Obtener los alumnos de la familia seleccionada
                alumnos = Alumnos.objects.filter(Familia_id=familia_id)
                # Actualizar las opciones del campo 'alumno'
                alumno_choices = [(alumno.id, f'{alumno.Nombres}') for alumno in alumnos]
                self.fields['alumno'].choices = alumno_choices