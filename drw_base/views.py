from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render
from .models import Drw
from django.shortcuts import render, get_object_or_404
from .forms import DrwForm
from .forms import NameForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_base/drw_list.html',{'drws': drws})
    
def drw_detail(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    return render(request, 'drw_base/drw_detail.html', {'drw': drw})
    
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

def drw_search(request):
    global SzukajLancucha
    #SzukanyLancuch = query
    #drws = Drw.objects.filter(nr_rys='1-4-3568').order_by('nr_rys')
    drws = Drw.objects.filter(nr_rys=SzukajLancucha).order_by('nr_rys')
    
    return render(request, 'drw_base/drw_search.html',{'drws': drws})


def get_szuk_lanc(request):
    global SzukajLancucha
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            #return HttpResponseRedirect('x')
            SzukajLancucha = form.cleaned_data['LancSzukany']
            #print(query)            
            return redirect( 'drw_search' )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'drw_base/drw_search_result.html', {'form': form})
