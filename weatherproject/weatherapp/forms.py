from django import forms


class SetMyCity(forms.Form):
    name = forms.CharField(label="Moje miasto", max_length=100)
