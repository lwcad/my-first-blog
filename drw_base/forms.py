from django import forms
 
from .models import Drw

 
class DrwForm(forms.ModelForm):
 

    class Meta:
        model = Drw
        fields = ('nr_rys', 'nr_arch', 'nazwa', 'opis', 'zweryfik',)
        
        labels = {
            "nr_rys":   "Nr rysunku",
            "nr_arch":  "Nr archiwalny",
            "nazwa":    "Nazwa",
            "opis":     "Opis - Uwagi",
            "zweryfik": "Rysunek zweryfikowany",
        }
        
class NameForm(forms.Form):
    LancSzukany = forms.CharField( label='Szukana wartość', max_length=150 )