from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def ecuaciones(request):
    return render(request, 'ecuaciones.html')

def biseccion(request):
    if request.method == 'POST':    #Si se envió un formulario
        f = request.POST['f']       #funcion
        a = request.POST['a']       #limite inferior
        b = request.POST['b']       #limite superior
        tol = request.POST['tol']   #tolerancia
        n = request.POST['n']       #iteraciones
        return redirect('biseccion_result', f=f, a=a, b=b, tol=tol, n=n)
    
    return render(request, 'biseccion.html')

def biseccion_result(request, f, a, b, tol, n,):
    
    if function(f, a) * function(f, b) > 0:
        error_msg = "Error: f(a) y f(b) deben tener signos opuestos"
        alert = "danger"
        return render(request, 'biseccion.html', {'error_msg': error_msg, 'alert': alert})
    
    c = a #c es el punto medio, lo inicializamos con a que es el limite inferior
    for i in range(n):
        #Calculamos el punto medio
        c = (a + b) / 2
        
        #Condicion de convergencia
        if function(f, c) == 0 or (b - a) / 2 < tol:
            error_msg = "El metodo converge"
            alert = "success"
            return render(request, 'biseccion_result.html', {'c': c, 'error_msg': error_msg, 'alert': alert})
        
        #Actualizamos los limites
        if function(f, a) * function(f, c) < 0:
            b = c
        else:
            a = c
        
    #Si el metodo no converge
    error_msg = "Error: El metodo no converge"
    alert = "danger"    

    return render(request, 'biseccion_result.html', {'c': c, 'error_msg': error_msg, 'alert': alert})

def regla_falsa(request):
    return render(request, 'regla_falsa.html')

def punto_fijo(request):
    return render(request, 'punto_fijo.html')

def newton(request):
    return render(request, 'newton.html')

def raices_multiples(request):
    return render(request, 'raices_multiples.html')

def secante(request):
    return render(request, 'secante.html')

def function(function, x):
    #Reemplaza x por el valor de x
    replaced_function = function.replace("x", "(" + str(x) + ")")   
    
    #eval() evalua la expresion
    return eval(replaced_function)  

    