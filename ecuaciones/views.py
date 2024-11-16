from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from django.http import HttpResponse
from sympy import symbols, diff

# Create your views here.
def ecuaciones(request):
    return render(request, "ecuaciones.html")


def biseccion(request, error_msg=None, alert=None):
    if request.method == "POST":  # Si se envió un formulario
        f = request.POST["f"]   # funcion
        a = request.POST["a"]   # limite inferior
        b = request.POST["b"]   # limite superior
        tol = request.POST["tol"]  # tolerancia
        n = 100  # iteraciones

        return redirect("biseccion_result", f=f, a=a, b=b, tol=tol, n=n)

    if error_msg is not None:
        return render(
            request, "biseccion.html", {"error_msg": error_msg, "alert": alert}
        )

    return render(request, "biseccion.html")


def biseccion_result(request, f, a, b, tol, n):
    tol = float(tol)
    a = float(a)
    b = float(b)

    if function(f, a) * function(f, b) > 0:
        error_msg = "Error: f(a) y f(b) deben tener signos opuestos"
        alert = "danger"
        return redirect("biseccion", error_msg=error_msg, alert=alert)
    
    # Verificar si a es menor que b
    if a > b:
        error_msg = "Error: a debe ser menor que b"
        alert = "danger"
        return redirect("biseccion", error_msg=error_msg, alert=alert)

    c = a  # Punto medio
    prev_c = None
    error_abs = None
    error_rel = None
    num_iteraciones = 0
    iteraciones = []
    valores_c = []

    for i in range(n):
        num_iteraciones += 1  # Contamos cada iteración
        c = (a + b) / 2
        iteraciones.append(i)
        valores_c.append(c)

        # Si se supera el limite de iteraciones
        if i == n - 1:
            error_msg = "Error: Se superó el número máximo de iteraciones (100)"
            alert = "danger"
            return redirect("biseccion", error_msg=error_msg, alert=alert)

        # Calcular errores relativo y absoluto
        if prev_c is not None:
            error_abs = abs(c - prev_c)
            error_rel = abs(error_abs / c) if c != 0 else None

        # Verificar si se cumple el criterio de parada
        if function(f, c) == 0 or (b - a) / 2 < tol:
            error_msg = "El método converge"
            alert = "success"
            break

        # Actualizar los valores de a y b
        if function(f, a) * function(f, c) < 0:
            b = c
        else:
            a = c

        prev_c = c

    # Generar la gráfica de la convergencia
    plt.figure()
    plt.plot(iteraciones, valores_c, marker="o", color="b")
    plt.xlabel("Iteraciones")
    plt.ylabel("Valor de c")
    plt.title("Convergencia del Método de Bisección")

    # Guardar la gráfica como una imagen en formato Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return render(
        request,
        "biseccion_result.html",
        {
            "c": c,
            "error_abs": error_abs,
            "error_rel": error_rel,
            "error_msg": error_msg,
            "alert": alert,
            "grafica": grafica_base64,
            "num_iteraciones": num_iteraciones,  # Pasamos el número de iteraciones
        },
    )


def regla_falsa(request, error_msg=None, alert=None):
    if request.method == "POST":  # Si se envió un formulario
        f = request.POST["f"]  # funcion
        a = request.POST["a"]  # limite inferior
        b = request.POST["b"]  # limite superior
        tol = request.POST["tol"]  # tolerancia
        n = 100  # iteraciones

        return redirect("regla_falsa_result", f=f, a=a, b=b, tol=tol, n=n)

    if error_msg is not None:
        return render(
            request, "regla_falsa.html", {"error_msg": error_msg, "alert": alert}
        )

    return render(request, "regla_falsa.html")


def regla_falsa_result(request, f, a, b, tol, n):
    tol = float(tol)
    a = float(a)
    b = float(b)
    
    # Verificar si el método es aplicable
    if function(f, a) * function(f, b) > 0:
        error_msg = "Error: f(a) y f(b) deben tener signos opuestos"
        alert = "danger"
        return redirect("regla_falsa", error_msg=error_msg, alert=alert)
    
    # Verificar si a es menor que b
    if a > b:
        error_msg = "Error: a debe ser menor que b"
        alert = "danger"
        return redirect("regla_falsa", error_msg=error_msg, alert=alert)
    
    c = a  # Inicializamos c
    prev_c = None
    error_abs = None
    error_rel = None
    num_iteraciones = 0
    iteraciones = []
    valores_c = []
    
    # Ciclo de iteración para el método de Regla Falsa
    for i in range(n):
        num_iteraciones += 1  # Contamos cada iteración
        
        # Calcular el valor de c usando la Regla Falsa
        c = b - (function(f, b) * (a - b)) / (function(f, a) - function(f, b))
        iteraciones.append(i)
        valores_c.append(c)

        # Si se supera el límite de iteraciones
        if i == n - 1:
            error_msg = "Error: Se superó el número máximo de iteraciones (100)"
            alert = "danger"
            return redirect("regla_falsa", error_msg=error_msg, alert=alert)
        
        # Calcular errores relativo y absoluto
        if prev_c is not None:
            error_abs = abs(c - prev_c)
            error_rel = abs(error_abs / c) if c != 0 else None

        # Verificar si se cumple el criterio de parada
        if abs(function(f, c)) < tol:
            error_msg = "El método converge"
            alert = "success"
            break
        
        # Actualizar los valores de a y b para la siguiente iteración
        if function(f, a) * function(f, c) < 0:
            b = c
        else:
            a = c

        prev_c = c
    
    # Generar la gráfica de la convergencia
    plt.figure()
    plt.plot(iteraciones, valores_c, marker="o", color="b")
    plt.xlabel("Iteraciones")
    plt.ylabel("Valor de c")
    plt.title("Convergencia del Método de Regla Falsa")

    # Guardar la gráfica como una imagen en formato Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    
    return render(
        request,
        "regla_falsa_result.html",
        {
            "c": c,
            "error_abs": error_abs,
            "error_rel": error_rel,
            "error_msg": 0,
            "alert": 0,
            "grafica": grafica_base64,
            "num_iteraciones": num_iteraciones,  # Pasamos el número de iteraciones
        },
    )
    #return render(request, "regla_falsa_result.html", {"c": 0, "error_abs": 0, "error_rel": 0, "error_msg": 0, "alert": 0, "grafica": 0, "num_iteraciones": 0})



def punto_fijo(request, error_msg=None, alert=None):
    if request.method == "POST":
        g = request.POST["g"]
        x_origin = request.POST["x_origin"]
        tol = request.POST["tol"]
        n = 100

        num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64 = punto_fijo_result(g, x_origin, tol, n)
        
        return render(request, "punto_fijo.html", {"num_iteraciones": num_iteraciones, "error_msg": error_msg, "alert": alert, "x": x, "error_abs": error_abs, "error_rel": error_rel, "iteraciones": iteraciones, "valores_x": valores_x, "grafica": grafica_base64})
    
    if error_msg is not None:
        return render(request, "punto_fijo.html", {"error_msg": error_msg, "alert": alert})
    
    return render(request, "punto_fijo.html")

def punto_fijo_result(g, x_origin, tol, n):
    tol = float(tol)
    x_origin = float(x_origin)
    
    # Inicializamos las variables
    num_iteraciones = 0
    iteraciones = []
    x_prev = x_origin
    error_abs = None
    error_rel = None
    valores_x = []
    grafica_base64 = None
    
    for i in range(n):
        num_iteraciones += 1
        
        x = function(g, x_prev)
        iteraciones.append(i)
        valores_x.append(x)
        
        #Si diverge
        if abs(x) > 1e10:
            error_msg = "Error: El método diverge"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Si se supera el límite de iteraciones
        if i == n - 1:
            error_msg = "Error: Se superó el número máximo de iteraciones (100)"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Calcular errores relativo y absoluto
        if x_prev is not None:
            error_abs = abs(x - x_prev)
            error_rel = abs(error_abs / x) if x != 0 else None
            
        # Verificar si se cumple el criterio de parada
        if abs(x - x_prev) < tol:
            error_msg = "El método converge"
            alert = "success"
            break
            
        #actualizar el valor de x_prev
        x_prev = x
        
    #Generar la gráfica de la convergencia
    plt.figure()
    plt.plot(iteraciones, valores_x, marker="o", color="b")
    plt.xlabel("Iteraciones")
    plt.ylabel("Valor de x")
    plt.title("Convergencia del Método de Punto Fijo")
    
    
    # Guardar la gráfica como una imagen en formato Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    
    return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
    
def newton(request, error_msg=None, alert=None):
    if request.POST:
        f = request.POST.get("f")
        xOrigin = request.POST.get("xOrigin")
        tol = request.POST.get("tol")
        n = 100

        num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64 = newton_result(f, xOrigin, tol, n)
        
        return render(request, "newton.html", {"num_iteraciones": num_iteraciones, "error_msg": error_msg, "alert": alert, "x": x, "error_abs": error_abs, "error_rel": error_rel, "iteraciones": iteraciones, "valores_x": valores_x, "grafica": grafica_base64})
    
    if error_msg is not None:
        return render(request, "newton.html", {"error_msg": error_msg, "alert": alert})
    
    return render(request, "newton.html")

import matplotlib.pyplot as plt
import io
import base64
from sympy import symbols, diff

def newton_result(f, xOrigin, tol, n):
    # Calcular la derivada de la función
    x = symbols('x')
    f = eval(f)
    df = diff(f, x)
    
    tol = float(tol)
    xOrigin = float(xOrigin)
    
    # Inicializamos las variables
    num_iteraciones = 0
    iteraciones = []
    x_prev = xOrigin
    error_abs = None
    error_rel = None
    valores_x = []
    grafica_base64 = None  # Variable para almacenar la gráfica
    
    for i in range(n):
        num_iteraciones += 1
        
        # Calculamos el nuevo valor de x usando el método de Newton
        f_x = function(str(f), x_prev)   # Evaluamos f(x)
        df_x = function(str(df), x_prev)  # Evaluamos f'(x)
        
        # Verificamos que la derivada no sea cero para evitar división por cero
        if df_x == 0:
            error_msg = "Error: La derivada es cero, el método no puede continuar."
            alert = "danger"
            return num_iteraciones, error_msg, alert, x_prev, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        x = x_prev - f_x / df_x
        iteraciones.append(i)
        valores_x.append(x)
        
        # Si diverge
        if abs(x) > 1e10:
            error_msg = "Error: El método diverge"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Si se supera el límite de iteraciones
        if i == n - 1:
            error_msg = "Error: Se superó el número máximo de iteraciones (100)"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Calcular errores relativo y absoluto
        if x_prev is not None:
            error_abs = abs(x - x_prev)
            error_rel = abs(error_abs / x) if x != 0 else None
            
        # Verificar si se cumple el criterio de parada
        if abs(x - x_prev) < tol:
            error_msg = "El método converge"
            alert = "success"
            break
            
        # Actualizar el valor de x_prev
        x_prev = x
    
    # Crear gráfica con los valores de x por iteración
    plt.figure(figsize=(8, 5))
    plt.plot(iteraciones, valores_x, marker="o", color="b", label="Valores de x")
    plt.title("Convergencia del Método de Newton", fontsize=14)
    plt.xlabel("Iteraciones", fontsize=12)
    plt.ylabel("Valor de x", fontsize=12)
    plt.grid(True)
    plt.legend()
    
    # Guardar la gráfica en formato Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    
    return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64


def raices_multiples(request):
    if request.POST:
        f = request.POST.get("f")
        xOrigin = request.POST.get("xOrigin")
        tol = request.POST.get("tol")
        n = 100

        num_iteraciones, error_msg, alert, x, error_abs, iteraciones, valores_x, grafica_base64 = raices_multiples_result(f, xOrigin, tol, n)
        
        return render(request, "raices_multiples.html", {"num_iteraciones": num_iteraciones, "error_msg": error_msg, "alert": alert, "x": x, "error_abs": error_abs, "iteraciones": iteraciones, "valores_x": valores_x, "grafica": grafica_base64})
    
    return render(request, "raices_multiples.html")


def raices_multiples_result(f, xOrigin, tol, n):
    # Calcular la derivada de la función
    x = symbols('x')
    f = eval(f)
    df = diff(f, x)          # Primera derivada
    ddf = diff(df, x)        # Segunda derivada
    
    tol = float(tol)
    xOrigin = float(xOrigin)
    
    # Inicializamos las variables
    num_iteraciones = 0
    iteraciones = []
    x_prev = xOrigin
    error_abs = None
    error_rel = None
    valores_x = []
    grafica_base64 = None  # Variable para almacenar la gráfica
    
    for i in range(n):
        num_iteraciones += 1
        
        f_x = function(str(f), x_prev)       # Evaluamos f(x)
        df_x = function(str(df), x_prev)    # Evaluamos f'(x)
        ddf_x = function(str(ddf), x_prev)  # Evaluamos f''(x)
        
        # Verificamos que f'(x)^2 - f(x)f''(x) no sea cero
        denominator = df_x**2 - f_x * ddf_x
        if denominator == 0:
            error_msg = "Error: Denominador igual a cero, el método no puede continuar."
            alert = "danger"
            return num_iteraciones, error_msg, alert, x_prev, error_abs, iteraciones, valores_x, grafica_base64
        
        # Calcular el nuevo valor de x
        x = x_prev - (f_x * df_x) / denominator
        iteraciones.append(i)
        valores_x.append(x)
        
                # Si diverge
        if abs(x) > 1e10:
            error_msg = "Error: El método diverge"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Si se supera el límite de iteraciones
        if i == n - 1:
            error_msg = "Error: Se superó el número máximo de iteraciones (100)"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Calcular errores relativo y absoluto
        if x_prev is not None:
            error_abs = abs(x - x_prev)
            error_rel = abs(error_abs / x) if x != 0 else None
        
        # Verificar criterio de parada
        if error_abs < tol:
            error_msg = "El método converge"
            alert = "success"
            break
        
        x_prev = x
    
    # Generar gráfica
    plt.figure(figsize=(8, 5))
    plt.plot(iteraciones, valores_x, marker="o", color="b", label="Valores de x")
    plt.title("Convergencia del Método de Raíces Múltiples", fontsize=14)
    plt.xlabel("Iteraciones", fontsize=12)
    plt.ylabel("Valor de x", fontsize=12)
    plt.grid(True)
    plt.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    
    return num_iteraciones, error_msg, alert, x, error_abs, iteraciones, valores_x, grafica_base64



def secante(request):
    if request.POST:
        f = request.POST.get("f")
        x_zero = request.POST.get("x_zero")
        x_one = request.POST.get("x_one")
        tol = request.POST.get("tol")
        n = 100

        num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64 = metodo_secante(f, x_zero, x_one, tol, n)
        
        return render(request, "secante.html", {"num_iteraciones": num_iteraciones, "error_msg": error_msg, "alert": alert, "x": x, "error_rel": error_rel, "error_abs": error_abs, "iteraciones": iteraciones, "valores_x": valores_x, "grafica": grafica_base64})
    
    return render(request, "secante.html")


def metodo_secante(f, x_zero, x_one, tol, n):
    f = function(str(f), symbols("x"))
    
    tol = float(tol)
    x_zero = float(x_zero)
    x_one = float(x_one)
    
    # Inicializamos las variables
    x = None
    num_iteraciones = 0
    iteraciones = []
    error_abs = None
    error_rel = None
    valores_x = []
    grafica_base64 = None  # Variable para almacenar la gráfica
    
    for i in range(n):
        num_iteraciones += 1
        
        f_x_zero = function(str(f), x_zero)  # f(x_zero)
        f_x_one = function(str(f), x_one)  # f(x_one)
        
        # Verificamos que f(x_one) - f(x_zero) no sea cero
        denominator = f_x_one - f_x_zero
        if denominator == 0:
            error_msg = "Error: División por cero, el método no puede continuar."
            alert = "danger"
            return num_iteraciones, error_msg, alert, x_one, error_abs, iteraciones, valores_x, grafica_base64
        
        # Calcular el nuevo valor de x
        x = x_one - f_x_one * (x_one - x_zero) / denominator
        iteraciones.append(i)
        valores_x.append(x)
        
                        # Si diverge
        if abs(x) > 1e10:
            error_msg = "Error: El método diverge"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Si se supera el límite de iteraciones
        if i == n - 1:
            error_msg = "Error: Se superó el número máximo de iteraciones (100)"
            alert = "danger"
            return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64
        
        # Calcular errores relativo y absoluto
        if x_one is not None:
            error_abs = abs(x - x_one)
            error_rel = abs(error_abs / x) if x != 0 else None
        
        # Verificar criterio de parada
        if error_abs < tol:
            error_msg = "El método converge"
            alert = "success"
            break
        
        x_zero = x_one
        x_one = x
    
    # Generar gráfica
    plt.figure(figsize=(8, 5))
    plt.plot(iteraciones, valores_x, marker="o", color="g", label="Valores de x")
    plt.title("Convergencia del Método de la Secante", fontsize=14)
    plt.xlabel("Iteraciones", fontsize=12)
    plt.ylabel("Valor de x", fontsize=12)
    plt.grid(True)
    plt.legend()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    grafica_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    
    return num_iteraciones, error_msg, alert, x, error_abs, error_rel, iteraciones, valores_x, grafica_base64



def function(function, x):
    # Reemplaza x por el valor de x
    replaced_function = function.replace("x", "(" + str(x) + ")")

    # eval() evalua la expresion
    return eval(replaced_function)
