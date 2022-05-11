from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Drw
from .forms import DrwForm, NameForm, NewUserForm
from django.http import FileResponse, Http404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator


# Create your views here.

#----------------------------------------------------------------------------
# lista rysunków nie stronicowana - nie używana obecnie
def drw_list(request):
    drws = Drw.objects.all().order_by('nr_rys')
    return render(request, 'drw_base/drw_list.html',{'drws': drws})
    
#----------------------------------------------------------------------------
def drw_list_paginate(request):
    drws = Drw.objects.all().order_by('nr_rys')
    iloscWierszyNaStronie = 10

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
#def drw_search_result(request):
#    global SzukajLancucha
#    drws = Drw.objects.filter(nr_rys__contains=SzukajLancucha).order_by('nr_rys')
#    iloscRysZnalez = len(drws)
#    return render(request, 'drw_base/drw_search_result.html',{'drws': drws,'iloscRysZnalez':iloscRysZnalez} )    

def drw_search_result(request):
    global SzukajLancucha, SzukajWpolu
    
    if SzukajWpolu == 'nr_rys' :     #'nr_rys':
        drws = Drw.objects.filter(nr_rys__contains=SzukajLancucha).order_by('nr_rys')
    elif SzukajWpolu == 'nazwa' :    # 'nazwa'
        drws = Drw.objects.filter(nazwa__contains=SzukajLancucha).order_by('nazwa')
    else:                            # 'nr_arch'
        drws = Drw.objects.filter(nr_arch__contains=SzukajLancucha).order_by('nr_arch')

    iloscRysZnalez = len(drws)
    iloscWierszyNaStronie = 15

    paginator = Paginator(drws, iloscWierszyNaStronie)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drw_base/drw_search_result.html',{'page_obj': page_obj,'iloscRysZnalez':iloscRysZnalez})

#----------------------------------------------------------------------------
def get_szuk_lanc(request):
    global SzukajLancucha, SzukajWpolu
    SzukajLancucha = ''
    SzukajWpolu = ''

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            SzukajLancucha = form.cleaned_data['LancSzukany']
            SzukajWpolu    = form.cleaned_data['szukaj_w_polu']
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
    filename='C:\\djangogirls\\proby_lw\\baza_rys_2022_05_05__10_07.txt'
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
#def drw_niezweryfik_list(request):
#    drws = Drw.objects.filter(zweryfik=False).order_by('nr_rys')
#    return render(request, 'drw_base/drw_niezweryfik_list.html', {'drws': drws})
def drw_niezweryfik_list(request):
    drws = Drw.objects.filter(zweryfik=False).order_by('nr_rys')
    iloscWierszyNaStronie = 10

    paginator = Paginator(drws, iloscWierszyNaStronie)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drw_base/drw_niezweryfik_list.html',{'page_obj': page_obj})    
    
#----------------------------------------------------------------------------
def drw_weryfikuj(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    drw.weryfikuj()
    return redirect('drw_base/drw_detail', pk=pk) # na djangogirls było bez 'drw_base/'
    
#----------------------------------------------------------------------------
def drw_remove(request, pk):
    drw = get_object_or_404(Drw, pk=pk)
    drw.delete()
    return redirect('drw_base/drw_list_paginate')


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

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Rejestracja zakończona sukcesem." )
			return redirect('get_szuk_lanc')
		messages.error(request, 'Nie udało się zarejestrować. Głędne dane.')
	form = NewUserForm()
	return render (request=request, template_name='drw_base/register.html', context={'register_form':form})

#----------------------------------------------------------------------------

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f'Zalogowałeś się jako {username}.')
				return redirect('get_szuk_lanc')
			else:
				messages.error(request,'Błędna nazwa użytkownika lub hasło.')
		else:
			messages.error(request,'Błędna nazwa użytkownika lub hasło.')
	form = AuthenticationForm()
	return render(request=request, template_name='drw_base/login.html', context={"login_form":form})

#----------------------------------------------------------------------------

def logout_request(request):
	logout(request)
	messages.info(request, 'Wylogowałeś się.') 
	return redirect('get_szuk_lanc')
#----------------------------------------------------------------------------