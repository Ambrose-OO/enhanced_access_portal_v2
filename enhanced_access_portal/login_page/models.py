from django.db import models
from datetime import date

# Create your models here.
class User(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  emailaddress = models.CharField(max_length=255, default = "example@example.com")
  password = models.CharField(max_length=255)
  joined_date = models.DateField(default = date.today) # https://www.geeksforgeeks.org/datefield-django-models/
  user_type = models.CharField(max_length=255)