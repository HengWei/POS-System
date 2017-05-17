from django.shortcuts import render

# Create your views here.


def report(request):
    return render(request, 'report.html',locals)