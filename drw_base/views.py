from django.shortcuts import render

# Create your views here.
def drw_list(request):
    return render(request, 'drw_base/drw_list.html',{})