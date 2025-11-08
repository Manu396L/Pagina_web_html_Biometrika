from django import forms
from django.contrib.auth.models import User
from .models import Profile, Personal, Ubicacion, Dispositivo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password2']
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth']

class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = [
            'nombre', 'apellido', 'dni', 'telefono', 'email',
            'cargo', 'fecha_ingreso', 'activo', 'ubicacion'  # 👈 campo agregado
        ]
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }
        
class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = [
            'tipo_ubicacion',
            'nombre_sede',
            'codigo_unico',
            'direccion',
            'descripcion',
            'dispositivo_biometrico',
            'nivel_seguridad',
        ]
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

#===============================================================
#                   DISPO
#================================================================
class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = [
            'nombre', 'numero_serie', 'tipo_sede', 'ubicacion', 
            'direccion_fisica', 'direccion_ip', 'zona_horaria',
            'intervalo_solicitud', 'estado', 'tipo_dispositivo', 'observaciones'
        ]
        widgets = {
            'direccion_fisica': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ej: Planta Baja, Edificio A'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notas adicionales sobre el dispositivo'}),
        }