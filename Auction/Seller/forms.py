from django import forms
from .models import Product, SellerDetail
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User

class pUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'category',
            'subcategory',
            'start',
            'end',
            'price',
            'description',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'image6',
        ]

    def __init__(self, *args, **kwargs):
                super(pUpdateForm,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False

class profileForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        help_texts = {
            'username':None,
        }

    def __init__(self, *args, **kwargs):
                super(profileForm1,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False
                

class UserForm1(forms.ModelForm):
        photo=forms.ImageField(widget=forms.FileInput)
        class Meta:
            model = SellerDetail
            fields = ['mobile','alternate_mobile','address','dob','sex','state','city','photo','locality','pincode']
            widgets ={
                'dob':forms.DateInput(attrs={'type':'date'}),
                'address':forms.Textarea(attrs={'rows':4}),
                
                
            }

        def __init__(self, *args, **kwargs):
                super(UserForm1,self).__init__(*args,**kwargs)
                self.helper = FormHelper()
                self.helper.form_show_labels = False
               
                
                