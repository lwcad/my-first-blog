from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import render

#może to jedno niżej już nie potrzebne ?
#from django.db import models

from .models import Drw
from django.shortcuts import render, get_object_or_404
from .forms import DrwForm
from .forms import NameForm
#from django.http import HttpResponse, HttpResponseRedirect
from django.http import FileResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# Create your views here.

#----------------------------------------------------------------------------
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_base/drw_list.html',{'drws': drws})
    
#----------------------------------------------------------------------------
def drw_list_paginate(request):
    drws = Drw.objects.all().order_by('nr_rys')
    iloscWierszyNaStronie = 3

    paginator = Paginator(drws, iloscWierszyNaStronie)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drw_base/drw_list_paginate.html',{'page_obj': page_obj})

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
    drws = Drw.objects.filter(nr_rys__contains=SzukajLancucha).order_by('nr_rys')
    iloscRysZnalez = len(drws)

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
        

#----------------------------------------------------------------------------
def delete_everything(self):
    Drw.objects.all().delete()

#----------------------------------------------------------------------------
def serwis(request):
    
    # importowanie do bazy z pliku tekstowego - Początek
    me = User.objects.get(username='wieslaw.legucki')

    # czytam dane z pliku 
    filename='C:\\djangogirls\\proby_lw\\baza_rys_2022_04_07__08_21.txt'
    #filename='C:\\djangogirls\\proby_lw\\baza_rys_2022_04_07__08_21-oryginal.txt'
    
    f=open(filename,'r')  # open file for reading
    arrRys=f.readlines()  # store the entire file in a variable
    f.close()
    i = 0
    tabRecordRys = ["0", "1", "2", "3", "4"]

    for pole in arrRys:
        #tabRecordRys[i] = "'" + pole.strip() + "'"
        tabRecordRys[i] = pole.strip()  # strip - chyba usuwam enter na końcu linii i też jak alltrim chyba
        i+=1
        if i == 5 :
            i = 0
            if tabRecordRys[4] == 'False':
                czySprawdzony=False
            else:
                czySprawdzony=True
            #tworzę nowy rekord w bazie
            Drw.objects.create( wprowadzil=me, nr_arch=tabRecordRys[0], nr_rys=tabRecordRys[1], nazwa=tabRecordRys[2], opis=tabRecordRys[3], zweryfik=czySprawdzony,  data_wprow  = timezone.now() )
    # importowanie do bazy z pliku tekstowego - Koniec
    
    """
    #kasuję zawartość tabeli Drw
    #delete_everything # coś nie działa
    Drw.objects.all().delete() # tak też można bez funkcji i to działa
    """
    
    return render(request, 'drw_base/serwis.html')

#----------------------------------------------------------------------------
def drw_niezweryfik_list(request):
    drws = Drw.objects.filter(zweryfik=False).order_by('nr_rys')
    return render(request, 'drw_base/drw_niezweryfik_list.html', {'drws': drws})
    
#----------------------------------------------------------------------------
def drw_weryfikuj(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    drw.weryfikuj()
    return redirect('drw_detail', pk=pk)
    
#----------------------------------------------------------------------------
def drw_remove(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    drw.delete()
    return redirect('drw_list')


#----------------------------------------------------------------------------
# to chyba przykład kasowania całej tabeli w bazie
"""
def drop_table(self):
    cursor = connection.cursor()
    table_name = self.model._meta.db_table
    sql = "DROP TABLE %s;" % (table_name, )
    cursor.execute(sql)
"""
#----------------------------------------------------------------------------



