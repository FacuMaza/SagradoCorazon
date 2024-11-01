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

class CuotasForm(forms.ModelForm):
    class Meta:
        model = Cuotas
        fields = '__all__'

        widgets = {
            'Alumnos': forms.Select(attrs={'class': 'form-control'}),
            'Tutor': forms.Select(attrs={'class': 'form-control'}),
            'Año': forms.NumberInput(attrs={'class': 'form-control'}),
            'Mes': forms.TextInput(attrs={'class': 'form-control'}),
            'Fecha_hora_del_pago': forms.DateInput(attrs={'class': 'form-control'}),
            'Monto_cuota': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class PagocuotaForm(forms.ModelForm):
    class Meta:
        model = pagocuota
        fields = ['efectivo', 'transferencia', 'cheque', 'pagare']
        widgets = {
            'efectivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'transferencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'cheque': forms.NumberInput(attrs={'class': 'form-control'}),
            'pagare': forms.NumberInput(attrs={'class': 'form-control'}),
        }