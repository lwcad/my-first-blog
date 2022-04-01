from django import forms
 
from .models import Drw
 
class DrwForm(forms.ModelForm):
 
    class Meta:
        model = Drw
        fields = ('nr_rys', 'nr_arch', 'nazwa', 'opis', 'zweryfik',)
         