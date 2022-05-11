from django import forms
from .models import Drw
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



NrCzyNazwa= [
    ('nr_rys', 'Nr rysunku'),
    ('nazwa' , 'Nazwa'),
    ('nr_arch', 'Nr archiwalny'),
    ]


 
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

#-----------------------------------------------------------------------------------------------------------------------        
class NameForm(forms.Form):
    LancSzukany   = forms.CharField( label='Szukana wartość', max_length=150 )
    szukaj_w_polu = forms.CharField( label='', widget=forms.RadioSelect(choices=NrCzyNazwa) , initial='nr_rys')

#-----------------------------------------------------------------------------------------------------------------------
class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

#-----------------------------------------------------------------------------------------------------------------------        
        