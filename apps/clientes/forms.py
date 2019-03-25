from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from apps.clientes.models import Cliente, Membresia, Operacion


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'nombre',
            'telefono',
            'genero',
            'marca',
            'modelo',
            'color',
            'matricula',
        )

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        fields = (
            'cliente',
            'tipoMembresia',
        )

    def __init__(self, *args, **kwargs):
        super(MembresiaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class OperacionForm(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = (
            'Membresia',
            'tipoOperacion',
            'descuento',
            'observaciones'
        )