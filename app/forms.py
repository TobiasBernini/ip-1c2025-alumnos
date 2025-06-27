from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput) #para ingresar la primera contraseña 
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)#para confirmar que se escribio bien la contraseña anterior

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']#esto se pide en el formulario

    def clean_password2(self):#valida si las contraseñas ingresadas son iguales 
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')#ve que no exista usuario repetido 
        if User.objects.filter(username=username).exists():#avisa que ya existe ese nombre de usuario y tira error  
            raise forms.ValidationError("Ese nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')# ve que el mail no se repita
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ese correo ya está en uso.")#si se repite tira este error 
        return email
