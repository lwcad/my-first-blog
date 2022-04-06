from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render
from .models import Drw
from django.shortcuts import render, get_object_or_404
from .forms import DrwForm
from .forms import NameForm
#from django.http import HttpResponse, HttpResponseRedirect
from django.http import FileResponse, Http404

# Create your views here.

#----------------------------------------------------------------------------
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_base/drw_list.html',{'drws': drws})

#----------------------------------------------------------------------------    
def drw_detail(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    return render(request, 'drw_base/drw_detail.html', {'drw': drw})
    
#----------------------------------------------------------------------------
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

#----------------------------------------------------------------------------
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

#----------------------------------------------------------------------------
def drw_search_result(request):
    global SzukajLancucha
    #drws = Drw.objects.filter(nr_rys=SzukajLancucha).order_by('nr_rys')
    drws = Drw.objects.filter(nr_rys__contains=SzukajLancucha).order_by('nr_rys')
    iloscRysZnalez = len(drws)
    #return render(request, 'drw_base/drw_search_result.html',{'drws': drws})
    return render(request, 'drw_base/drw_search_result.html',{'drws': drws,'iloscRysZnalez':iloscRysZnalez} )    

#----------------------------------------------------------------------------
def get_szuk_lanc(request):
    global SzukajLancucha
    SzukajLancucha = ''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            SzukajLancucha = form.cleaned_data['LancSzukany']
            return redirect( 'drw_search_result' )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'drw_base/drw_search.html', {'form': form})

#----------------------------------------------------------------------------
def pdf_view(request, pk):
   
    drw = get_object_or_404(Drw, pk=pk)

    podstawaSciezki      = 'Y:/rys_arch_nt/'
    nrArchiwalny         = drw.nr_arch.replace(".", "_")
    katalog              = nrArchiwalny[0:9] + "_/"
    pelnaSciezkaPlikuPdf = podstawaSciezki + katalog + nrArchiwalny + ".pdf"
    
    try:
        return FileResponse(open(pelnaSciezkaPlikuPdf, 'rb'), content_type='application/pdf')        

    except FileNotFoundError:
        raise Http404()