from django import forms 
from ca.models import UserCust,Donate,SponserTable
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserCust
        fields=['fname','lname','emailaddress','gender','phone_number','location','addresss','username']
        
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    
class DonateForm(forms.ModelForm):
    class Meta:
        model=Donate
        fields = ['credict_cardno','exp','ccv','amount']
    
    # fname=forms.CharField()
    # lname=forms.CharField()
    # state=forms.CharField()
    # email=forms.CharField()
    # phoneno=forms.CharField()
    # amount=forms.CharField()

# class UserUpdateForm(forms.Form):
#     first_name=forms.CharField()
#     last_name=forms.CharField()
#     email=forms.CharField()
#     gender=forms.CharField()
#     phone_number=forms.CharField()
#     location=forms.CharField()
#     address=forms.CharField()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserCust
        fields = ['fname', 'lname', 'emailaddress', 'gender', 'phone_number', 'location','addresss' ]
        
class SponsorForm(forms.ModelForm):
    class Meta:
        model = SponserTable
        fields = ['user', 'child', 'sponsor_type', 'credit_cardno', 'exp', 'ccv', 'budget']
        

        

        

    
    
    
    
    
         