from django.shortcuts import render
from POSSys.models import Menu


# Create your views here.

def index(request):
    menuList = Menu.objects.filter(menuparentid=0)
    menu1 = Menu.objects.all().exclude(menuparentid=0)
    return render(request, 'index.html', locals())


def Check(request):
    return render(request, 'check.html', locals())
