from django.shortcuts import render

# Create your views here.
def ecuaciones(request):
    return render(request, 'ecuaciones.html')