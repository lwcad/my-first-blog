from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render
from .models import Drw
from django.shortcuts import render, get_object_or_404
from .forms import DrwForm


# Create your views here.
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_base/drw_list.html',{'drws': drws})
    
def drw_detail(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    return render(request, 'drw_base/drw_detail.html', {'drw': drw})
    
#def drw_new(request):
#    form = DrwForm()
#    return render(request, 'drw_base/drw_edit.html', {'form': form})

def drw_new(request):
    if request.method == "POST":
        form = DrwForm(request.POST)
        if form.is_valid():
            drw = form.save(commit=False)
            drw.wprowadzil = request.user
            drw.data_wprow = timezone.now()
            drw.save()
            return redirect('drw_detail', pk=drw.pk)
    else:
        form = DrwForm()
    return render(request, 'drw_base/drw_edit.html', {'form': form})

def drw_edit(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    if request.method == "POST":
        form = DrwForm(request.POST, instance=drw)
        if form.is_valid():
            drw = form.save(commit=False)
            drw.wprowadzil = request.user
            drw.data_wprow = timezone.now()
            drw.save()
            return redirect('drw_detail', pk=drw.pk)
    else:
        form = DrwForm(instance=drw)
    return render(request, 'drw_base/drw_edit.html', {'form': form})

