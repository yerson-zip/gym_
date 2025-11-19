from django import forms 

class LoginForm(forms.Form):
    correo   = forms.EmailField(label="Correo")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class UsuarioForm(forms.Form):
    nombre   = forms.CharField(max_length=100)
    correo   = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)



class ReservaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    actividad = forms.CharField(max_length=100)
    notas = forms.CharField(widget=forms.Textarea, required=False)

    