from django import forms

class InputForm(forms.Form):
    inputField = forms.CharField(max_length=280, widget=forms.TextInput(attrs={'id':'textInput'}))