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