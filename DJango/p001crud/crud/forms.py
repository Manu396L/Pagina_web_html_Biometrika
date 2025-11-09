from django import forms
from .models import Task
from .models import Edificio

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs= {'class': 'form-control'}),
            'description':forms.Textarea(attrs= {'class': 'form-control', 'rows':3})
        }

class EdificioForm(forms.ModelForm):
    class Meta:
        model = Edificio
        fields = ['nombre', 'direccion', 'descripcion']

    """empleados_autorizados = forms.ModelMultipleChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )"""