from django.shortcuts import render
from .models import Drw

# Create your views here.
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_base/drw_list.html',{'drws': drws})