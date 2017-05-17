from django.shortcuts import render
from POSSys.models import Menu


# Create your views here.

def index(request):
    r1 = Menu.GetList()

    return render(request, 'index.html', locals())
