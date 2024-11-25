from django import forms

class UploadImageForm(forms.Form):
    abd_image = forms.ImageField()
