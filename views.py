from django.shortcuts import render

def home(request):
    context = None
    return render(request, 'home.html', context)
