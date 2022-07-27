from logging import PlaceHolder
from random import choices
from tkinter import Widget
from django import forms
import django.forms.widgets
from django.forms import DateInput, ModelForm
from .models import HomeWork,Notes,Todo,User
from django.contrib.auth.forms import UserCreationForm
# Create the form class.
class NoteForm(ModelForm):
     class Meta:
         model = Notes
         fields = ['title', 'description']     
class HomeForm(ModelForm):
    class Meta: 
        model = HomeWork
        widgets = {'due': DateInput(attrs={'type': 'date'})}
        fields = ['subject','title','description','due','is_finished']
class Dashform(forms.Form):
    Text = forms.CharField(max_length=255, label="Enter You search:")
class Todoform(ModelForm): 
    class Meta:
        model= Todo
        fields =['title','is_finished']
class UserRegisterationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2']
class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField (choices=CHOICES,widget=forms.RadioSelect)
class ConversionLengthForm(forms.Form):
    CHOICES= [('yard','Yard'),('foot','Foot')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','Placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )  
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )  
class ConversionMassForm(forms.Form):
    CHOICES= [('pound','Pound'),('kilogram','Kilogram')]
    input = forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','Placeholder':'Enter the number'}
    ))
    measure1 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )  
    measure2 = forms.CharField(
        label = '',widget=forms.Select(choices=CHOICES)
    )  

  