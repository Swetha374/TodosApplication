from django import forms
from django.contrib.auth.models import User
from todoapp.models import Todos
from django.contrib.auth.forms import UserCreationForm

"""
there are two types of form normal form and model form
in normal form we should give one by one fields explicitely,form.save() method is not applicable
in model form we should mention model and fields inside meta class

"""
# class RegistrationForm(forms.Form):
#     first_name=forms.CharField()
#     last_name=forms.CharField()
#     username=forms.CharField()
#     email=forms.EmailField()
#     password=forms.CharField()
class RegistrationForm(UserCreationForm): #user creation form contail 2 passwords,1 for type and 1 for confirm. kure validations und
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 =forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"] #fname,lname..etc these are defined in user model->abstract user,we should give these fields exactly like that
        #widgets should be like this,widgets eg: password type cheyumbo kananthirikunath..etc
        widgets={
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"})) #attributes=add form-control class,adding for take text box complete width
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["task_name"]
        widgets={
            "task_name":forms.TextInput(attrs={"class":"form-control"})
        }

#edit form
class TodoChangeForm(forms.ModelForm):
    class Meta:
        model=Todos
        exclude=("user",)
