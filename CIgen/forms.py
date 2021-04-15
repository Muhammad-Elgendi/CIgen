from django import forms
from django.contrib.auth import get_user_model

class ContactForm(forms.Form):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={"id":"name","name":"name","class":"form-control","placeholder":"Your full name"}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"id":"email","name":"email","class":"form-control","placeholder":"Your email"}))
    subject = forms.CharField(required=False,widget=forms.TextInput(attrs={"id":"subject","name":"subject","class":"form-control","placeholder":"Subject of your message"}))
    message = forms.CharField(required=True,widget=forms.Textarea(attrs={"id":"message","name":"message","class":"form-control","placeholder":"Your message","rows":"3"}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.split()) < 2:
            raise forms.ValidationError("Name has to be a full name")
        return name


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"id":"email","name":"email","class":"form-control","placeholder":"Your email"}))
    password = forms.CharField(required=True,widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm password",required=True,widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords mush match.")
        return data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        User = get_user_model()
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("User name is taken")      
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email is already registered")      
        return email