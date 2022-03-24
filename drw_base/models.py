from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Drw(models.Model):
    wprowadzil  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # kto wprowadził do bazy
    nr_arch     = models.CharField(max_length=30)    # Nr archiwlny rysunku
    nr_rys      = models.CharField(max_length=30)    # Nr rysunku
    nazwa       = models.CharField(max_length=256)   # Nazwa rysunku    
    opis        = models.TextField()                 # Opis pole "Memo" z delphi
    zweryfik    = models.BooleanField(default=False) # Czy rysunek zweryfikowany
    data_wprow  = models.DateTimeField(
            default=timezone.now)                    # data wprowadzenia do bazy

    #def publish(self):
    #    self.published_date = timezone.now()
    #    self.save()

    def __str__(self):
        return 'Nr rysunku: ' + self.nr_rys