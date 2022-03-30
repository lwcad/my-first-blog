from django.shortcuts import render
from .models import Drw
from django.shortcuts import render, get_object_or_404

# Create your views here.
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_list.html',{'drws': drws})
    
def drw_detail(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    return render(request, 'drw_base/drw_detail.html', {'drw': drw})    