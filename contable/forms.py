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


class ExtrasForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=[('INGRESO', 'Ingreso'), ('EGRESO', 'Egreso')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo'
    )
    fecha = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        initial=date.today().strftime('%Y-%m-%d'),
        label='Fecha'
    )

    class Meta:
        model = extras
        fields = ['tipo', 'descripcion', 'monto', 'fecha']

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo")
        monto = cleaned_data.get("monto")

        if tipo == 'EGRESO' and not monto:
            raise forms.ValidationError("El monto es requerido para un egreso.")
        return cleaned_data