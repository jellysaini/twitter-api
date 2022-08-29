from email.policy import default
from django import forms


class FormSearchTweeterUser(forms.Form):
    query = forms.CharField(label='Find People')



class FormSearchTweet(forms.Form):
    query = forms.CharField(label='Search Tweet')

