from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import base64
import numpy as np


# Create your views here.
def ecuaciones(request):
    return render(request, "ecuaciones.html")


def biseccion(request, error_msg=None, alert=None):
    if request.method == "POST":  # Si se envió un formulario
        f = request.POST["f"]  # funcion
        a = int(request.POST["a"])  # limite inferior
        b = int(request.POST["b"])  # limite superior
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

    if function(f, a) * function(f, b) > 0:
        error_msg = "Error: f(a) y f(b) deben tener signos opuestos"
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
        a = int(request.POST["a"])  # limite inferior
        b = int(request.POST["b"])  # limite superior
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
    
    # Verificar si el método es aplicable
    if function(f, a) * function(f, b) > 0:
        error_msg = "Error: f(a) y f(b) deben tener signos opuestos"
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
            "grafica": 0,
            "num_iteraciones": num_iteraciones,  # Pasamos el número de iteraciones
        },
    )
    #return render(request, "regla_falsa_result.html", {"c": 0, "error_abs": 0, "error_rel": 0, "error_msg": 0, "alert": 0, "grafica": 0, "num_iteraciones": 0})



def punto_fijo(request):
    return render(request, "punto_fijo.html")


def newton(request):
    return render(request, "newton.html")


def raices_multiples(request):
    return render(request, "raices_multiples.html")


def secante(request):
    return render(request, "secante.html")


def function(function, x):
    # Reemplaza x por el valor de x
    replaced_function = function.replace("x", "(" + str(x) + ")")

    # eval() evalua la expresion
    return eval(replaced_function)
