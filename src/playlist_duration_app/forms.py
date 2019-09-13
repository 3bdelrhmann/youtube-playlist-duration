from django import forms
from .models import playlistLinkForm

class linkForm(forms.Form):
    link = forms.CharField(label='Playlist Link', max_length=200,
    	widget=forms.TextInput(attrs={'class' : 'form-control col-sm-12 text-center','autocomplete':'off'}))
