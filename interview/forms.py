from django import forms
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re


class UserRegForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder' : 'Enter Password'
        })
    )

    class Meta:

        model = User_tbl

        fields =[
            'name',
            'email',
            'phone',
            'image',
            'address'
        ]

        widgets = {

            'name' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Enter Your name'
            }),

            'email' : forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder' : "Enter your Email"
            }),

            'phone' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder' : "Enter your Phone number"
            }),

            'image' : forms.FileInput(attrs={
                'class': 'form-control',
            }),

            'address' : forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder' : "Enter your Address",
                'rows' : 3
            }),
        }


        #email Validation 

        def clean_email(self):

            email = self.cleaned_data['email']

            if User_tbl.objects.filter(email =email).exists():
                raise ValidationError(
                    "Email already exists"
                )
            

        def clean_phone(self):

            phone = self.cleaned_data['phone']

            if User_tbl.objects.filter(phone = phone).exists():
                raise ValidationError(
                    "Phone number already exists"
                )
            
        
        def clean_password(self):

            password = self.cleaned_data['password']

            if len(password) < 8:
                raise ValidationError(
                    "Password must be at least 8 characters long"
                )
            
            if not re.search(r'[A-Z]', password):
                raise ValidationError(
                    "Password must contain at least one uppercase letter"
                )
            
            if not re.search(r'[a-z]', password):
                raise ValidationError(
                    "Password must contain at least one lowercase letter"
                )
            
            if not re.search(r'\d', password):
                raise ValidationError(
                    "Password must contain at least one digit"
                )
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise ValidationError(
                    "Password must contain at least one special character"
                )

            
            validate_password(password)

            return password
        

class LoginForm(forms.Form):

    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )


from django import forms
from .models import *


class QuestionForm(forms.ModelForm):

    class Meta:

        model = Question

        fields = '__all__'

        widgets = {

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'correct_answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'marks': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }