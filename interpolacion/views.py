from django.shortcuts import render

# Create your views here.
def interpolacion(request):
    return render(request, 'interpolacion.html')