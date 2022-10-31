from pyexpat import model
from django.db import models
from django.forms import ModelForm
from .models import autionlisting

class auctionlisting_form(ModelForm):
    class Meta:
        model=autionlisting
        fields=['name','image','description','starting_bid','end_date']
