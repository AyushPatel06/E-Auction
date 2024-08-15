from django.forms import *
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field,Div
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes
from .models import ReviewRating, UserDetail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class profileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        help_texts = {
            'username':None,
        }

    def __init__(self, *args, **kwargs):
                super(profileForm,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False
                

class UserForm(ModelForm):
        photo=forms.ImageField(widget=forms.FileInput)
        class Meta:
            model = UserDetail
            fields = ['mobile','alternate_mobile','address','dob','sex','state','city','photo','locality','pincode']
            widgets ={
                'dob':forms.DateInput(attrs={'type':'date'}),
                'address':forms.Textarea(attrs={'rows':4}),
                
                
            }

        def __init__(self, *args, **kwargs):
                super(UserForm,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False
               
                

class addressForm(ModelForm):
        class Meta:
            model = UserDetail
            fields = ['mobile','alternate_mobile','address','state','city','locality','pincode']
            widgets ={
                'address':forms.Textarea(attrs={'rows':4}),  
            }

        def __init__(self, *args, **kwargs):
                super(addressForm,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False


class addressForm2(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
                super(addressForm2,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False
                
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review', 'rating']