from django.db import models
from django import forms

from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_type_choices = [ 
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    user_type = models.CharField(max_length=50, choices=user_type_choices, default='Admin') 

class SuperAdmin(CustomUser):
    is_available = models.BooleanField(default=True)

class UserCust(CustomUser):
    GENDER_CHOICES = (('male', 'Male'),('female', 'Female'),('other', 'Other'))
    fname=models.CharField(max_length=50,null=True)
    lname=models.CharField(max_length=50,null=True)
    emailaddress=models.EmailField(max_length=254,null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    location= models.CharField(max_length=30)
    addresss=models.TextField()
    phone_number=models.CharField(max_length=10)
    
class Donate(models.Model):
    personal_details=models.ForeignKey(UserCust,on_delete=models.CASCADE)
    credict_cardno=models.PositiveIntegerField()
    exp=models.DateField(auto_now=False, auto_now_add=False)
    ccv=models.CharField(max_length=3)
    def clean(self):
        if len(self.ccv) != 3 or not self.ccv.isdigit():
            raise forms.ValidationError("Field must be a 3-digit number without leading zeros.")
    amount=models.PositiveIntegerField()


class AdoptionRequest(models.Model):
    personal_details=models.ForeignKey(UserCust,on_delete=models.CASCADE)
    subject=models.CharField(max_length=150)
    isapproved=models.BooleanField(default=False)
    

class AdoptionFormView(models.Model):
    personal_details = models.ForeignKey(UserCust, on_delete=models.CASCADE,default=None)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    age = models.IntegerField()
    marital_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')])
    occupation = models.CharField(max_length=100)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    criminal_history = models.BooleanField()
    id_proof = models.FileField(upload_to='images/')  # New field for ID proof file
    additional_comments = models.TextField()
    isaccepted=models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)  # Feedback field for admin responses
    
    
class ChildDetails(models.Model):
    name=models.CharField(max_length=50)
    age=models.CharField(max_length=50)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True)
    since=models.PositiveIntegerField()
        
class ConformChild(models.Model):
    user=models.ForeignKey(UserCust, on_delete=models.CASCADE,default=None)
    child=models.ForeignKey(ChildDetails,on_delete=models.CASCADE)
    isapproved=models.BooleanField(default=False)
    
class SponserTable(models.Model):
    user = models.ForeignKey(UserCust, on_delete=models.CASCADE, default=None)
    child = models.ForeignKey(ChildDetails, on_delete=models.CASCADE)
    SPONSOR_TYPES = (
        ('medical', 'Medical'),
        ('clothings', 'Clothings'),
        ('education', 'Education'),
        ('sports', 'Sports'),
        ('food_and_nutrition', 'Food and Nutrition'),
    )
    sponsor_type = models.CharField(max_length=20, choices=SPONSOR_TYPES, null=True)
    credit_cardno = models.PositiveIntegerField()
    exp = models.DateField(auto_now=False, auto_now_add=False)
    ccv = models.CharField(max_length=3)
    budget = models.PositiveIntegerField()

    def clean(self):
        if len(self.ccv) != 3 or not self.ccv.isdigit():
            raise forms.ValidationError("Field must be a 3-digit number without leading zeros.")
    


    
    
    
    


