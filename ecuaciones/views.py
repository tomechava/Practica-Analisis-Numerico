from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def ecuaciones(request):
    return render(request, 'ecuaciones.html')

def biseccion(request):
    if request.method == 'POST':    #Si se envió un formulario
        f = request.POST['f']       #funcion
        a = int(request.POST['a'])       #limite inferior
        b = int(request.POST['b'])       #limite superior
        tol = float(request.POST['tol'])   #tolerancia
        n = 100       #iteraciones
    
        return redirect('biseccion_result', f=f, a=a, b=b, tol=tol, n=n)
    
    return render(request, 'biseccion.html')

def biseccion_result(request, f, a, b, tol, n):
    tol = float(tol)  # Convertir tol a float
    
    if function(f, a) * function(f, b) > 0:
        error_msg = "Error: f(a) y f(b) deben tener signos opuestos"
        alert = "danger"
        return render(request, 'biseccion.html', {'error_msg': error_msg, 'alert': alert})
    
    # Inicializamos c y los errores
    c = a  # Punto medio
    prev_c = None  # Variable para almacenar el valor anterior de c
    error_abs = None
    error_rel = None

    for i in range(n):
        # Calculamos el punto medio
        c = (a + b) / 2

        # Si prev_c no es None, calculamos los errores
        if prev_c is not None:
            error_abs = abs(c - prev_c)
            error_rel = abs(error_abs / c) if c != 0 else None
        
        # Condición de convergencia
        if function(f, c) == 0 or (b - a) / 2 < tol:
            error_msg = "El método converge"
            alert = "success"
            return render(request, 'biseccion_result.html', {'c': c, 'error_abs': error_abs, 'error_rel': error_rel, 'error_msg': error_msg, 'alert': alert})
        
        # Actualizamos los límites y el valor anterior de c
        if function(f, a) * function(f, c) < 0:
            b = c
        else:
            a = c

        prev_c = c  # Guardamos el valor actual de c como el valor previo

    # Si el método no converge en n iteraciones
    error_msg = "Error: El método no converge"
    alert = "danger"
    
    return render(request, 'biseccion_result.html', {'c': c, 'error_abs': error_abs, 'error_rel': error_rel, 'error_msg': error_msg, 'alert': alert})


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

    