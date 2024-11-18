from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from django.http import HttpResponse
from sympy import symbols, diff

# Create your views here.
def sistemas(request):
    return render(request, 'sistemas.html')

def gauss_parcial(request):
    if request.POST:
        # Obtener los datos del formulario
        columns = int(request.POST['columns'])
        rows = int(request.POST['rows'])
        A = np.zeros((rows, columns))
        
        for i in range(rows):
            for j in range(columns):
                A[i, j] = float(request.POST[f'A[{i}][{j}]'])
        
        b = np.zeros(rows)
        for i in range(rows):
            b[i] = float(request.POST[f'b[{i}]'])
        
        
        x, etapas, alert, error_msg = gauss_pivoteo_parcial(A, b)
        
        ultima = etapas[-1]
        
        return render(request, 'gauss_parcial.html', {'x': x, 'img_url': 0, 'alert': alert, 'error_msg': error_msg, 'etapas': etapas, 'columns': columns, 'rows': rows, 'ultima': ultima})
    
    return render(request, 'gauss_parcial.html')

def gauss_pivoteo_parcial(A, b):
    """
    Método de Gauss con Pivoteo Parcial para resolver un sistema de ecuaciones.
    
    Args:
        A: Matriz de coeficientes (numpy array).
        b: Vector de términos independientes (numpy array).
        
    Returns:
        x: Solución del sistema (numpy array).
        etapas: Lista de matrices A modificadas en cada etapa (para análisis o gráficos).
    """
    n = len(A)
    A = A.astype(float)     # Convertir a float para evitar errores de tipo
    b = b.astype(float)     # Convertir a float para evitar errores de tipo
    etapas = []
    alert = None
    error_msg = None
    
    # Validar si hay ceros en la diagonal principal antes de iniciar
    if any(np.diag(A) == 0):
        alert = "danger"
        error_msg = "Error: La matriz tiene ceros en la diagonal principal. Intente reorganizar las filas."
        return x, etapas, alert, error_msg
    
    # Matriz aumentada
    Ab = np.hstack([A, b.reshape(-1, 1)])       # Aumentar la matriz A con el vector b
    
    for k in range(n - 1):      # Iterar sobre las filas de la matriz
        # Pivoteo Parcial
        max_row = np.argmax(abs(Ab[k:, k])) + k     # Fila con el pivote más grande (absoluto)
        
        if Ab[max_row, k] == 0:     # Si el pivote es cero, no hay solución única
            error_msg = "Error: La matriz tiene ceros en la diagonal principal. Intente reorganizar las filas."
            alert = "danger"
            return x, etapas, alert, error_msg
        
        # Intercambiar filas
        if max_row != k:        # Si la fila con el pivote no es la actual
            Ab[[k, max_row]] = Ab[[max_row, k]]     # Intercambiar filas
        
        # Eliminación
        for i in range(k + 1, n):       # Iterar sobre las filas debajo de la actual
            factor = Ab[i, k] / Ab[k, k]        # Factor para hacer cero el elemento debajo del pivote
            Ab[i, k:] -= factor * Ab[k, k:]     # Restar la fila actual multiplicada por el factor
        
        etapas.append(Ab.copy())  # Guardar la matriz aumentada en cada etapa
    
    # Sustitución regresiva
    x = np.zeros(n)     # Vector para almacenar la solución
    
    for i in range(n - 1, -1, -1):      # Iterar desde la última fila hasta la primera
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:])) / Ab[i, i]       # Calcular el valor de la variable
    
    error_msg = "El sistema se resolvió correctamente."
    alert = "success"
    
    return x, etapas, alert, error_msg


def gauss_total(request):
    if request.POST:
        # Obtener los datos del formulario
        columns = int(request.POST['columns'])
        rows = int(request.POST['rows'])
        A = np.zeros((rows, columns))
        
        for i in range(rows):
            for j in range(columns):
                A[i, j] = float(request.POST[f'A[{i}][{j}]'])
        
        b = np.zeros(rows)
        for i in range(rows):
            b[i] = float(request.POST[f'b[{i}]'])
        
        x, etapas, cambios, error_msg, alert = gauss_pivoteo_total(A, b)
        
        ultima = etapas[-1]
        
        return render(request, 'gauss_total.html', {'x': x, 'img_url': 0, 'alert': alert, 'error_msg': error_msg, 'etapas': etapas, 'columns': columns, 'rows': rows, 'ultima': ultima, 'cambios': cambios})
    
    return render(request, 'gauss_total.html')

def gauss_pivoteo_total(A, b):
    """
    Método de Gauss con Pivoteo Total para resolver un sistema de ecuaciones.
    
    Args:
        A: Matriz de coeficientes (numpy array).
        b: Vector de términos independientes (numpy array).
        
    Returns:
        x: Solución del sistema (numpy array).
        etapas: Lista de matrices A modificadas en cada etapa (para análisis o gráficos).
        cambios: Lista de cambios de columnas realizados.
    """
    n = len(A)
    A = A.astype(float)     # Convertir a float para evitar errores de tipo
    b = b.astype(float)     # Convertir a float para evitar errores de tipo
    etapas = []     # Lista para guardar las matrices en cada etapa
    cambios = list(range(n))  # Para rastrear cambios de columnas
    error_msg = None
    alert = None
    
    # Validar si hay ceros en la diagonal principal antes de iniciar
    if any(np.diag(A) == 0):
        error_msg = "Error: La matriz tiene ceros en la diagonal principal. Intente reorganizar las filas."
        alert = "danger"
        return 0, 0, cambios, error_msg, alert
    
    # Matriz aumentada
    Ab = np.hstack([A, b.reshape(-1, 1)])       # Aumentar la matriz A con el vector b
    
    for k in range(n - 1):      # Iterar sobre las filas de la matriz
        # Pivoteo Total
        submat = abs(Ab[k:, k:n])  # Submatriz donde buscar el pivote
        max_row, max_col = np.unravel_index(np.argmax(submat), submat.shape)        # Fila y columna del pivote
        max_row += k        # Ajustar el índice de la fila
        max_col += k        # Ajustar el índice de la columna
        
        if Ab[max_row, max_col] == 0:       # Si el pivote es cero, no hay solución única
            alert = "danger"
            error_msg = "Error: La matriz tiene ceros en la diagonal principal. Intente reorganizar las filas."
            return 0, 0, cambios, error_msg, alert
        
        # Intercambiar filas
        if max_row != k:        # Si la fila con el pivote no es la actual
            Ab[[k, max_row]] = Ab[[max_row, k]]     # Intercambiar filas
        
        # Intercambiar columnas 
        if max_col != k:        # Si la columna con el pivote no es la actual
            Ab[:, [k, max_col]] = Ab[:, [max_col, k]]       # Intercambiar columnas
            cambios[k], cambios[max_col] = cambios[max_col], cambios[k]     # Actualizar lista de cambios
        
        # Eliminación
        for i in range(k + 1, n):       # Iterar sobre las filas debajo de la actual
            factor = Ab[i, k] / Ab[k, k]        # Factor para hacer cero el elemento debajo del pivote
            Ab[i, k:] -= factor * Ab[k, k:]     # Restar la fila actual multiplicada por el factor
        
        etapas.append(Ab.copy())  # Guardar la matriz aumentada en cada etapa
    
    # Sustitución regresiva
    x = np.zeros(n)     # Vector para almacenar la solución
    for i in range(n - 1, -1, -1):      # Iterar desde la última fila hasta la primera
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:])) / Ab[i, i]       # Calcular el valor de la variable
    
    # Reordenar la solución para que corresponda a las variables originales
    x_final = np.zeros(n)       # Vector para la solución reordenada
    for i, pos in enumerate(cambios):       # Iterar sobre los cambios de columnas
        x_final[pos] = x[i]     # Asignar el valor de la variable a la posición correcta
        
    error_msg = "El sistema se resolvió correctamente."
    alert = "success"
    
    return x_final, etapas, cambios, error_msg, alert

def doolittle(request):
    if request.POST:
        # Obtener los datos del formulario
        columns = int(request.POST['columns'])
        rows = int(request.POST['rows'])
        A = np.zeros((rows, columns))
        
        for i in range(rows):
            for j in range(columns):
                A[i, j] = float(request.POST[f'A[{i}][{j}]'])
        
        L, U, error_msg, alert = factorizacion_lu_doolittle(A)
        
        return render(request, 'doolittle.html', {'L': L, 'U': U, 'alert': alert, 'error_msg': error_msg, 'columns': columns, 'rows': rows})
    
    return render(request, 'doolittle.html')

def factorizacion_lu_doolittle(A):
    """
    Realiza la factorización LU de una matriz A utilizando el método de Doolittle.
    
    Parámetros:
        A: numpy.ndarray
            Matriz cuadrada que será factorizada.
            
    Retorna:
        L: numpy.ndarray
            Matriz triangular inferior con unos en la diagonal.
        U: numpy.ndarray
            Matriz triangular superior.
        error_msg: str
            Mensaje de error si la factorización falla.
        alert: str
            Tipo de alerta ('danger' si hay error, 'success' si todo va bien).
    """
    error_msg = None
    alert = None
    
    # Verificar si la matriz es cuadrada
    n, m = A.shape
    if n != m:
        error_msg = "Error: La matriz no es cuadrada."
        alert = "danger"
        return None, None, error_msg, alert

    # Inicializar matrices L y U
    L = np.eye(n)  # Matriz identidad (unos en la diagonal)
    U = np.zeros((n, n))  # Matriz de ceros

    # Realizar la factorización
    for i in range(n):
        # Verificar si hay un cero en la diagonal principal
        if A[i, i] == 0:
            error_msg = "Error: La matriz tiene ceros en la diagonal principal."
            alert = "danger"
            return None, None, error_msg, alert

        # Calcular elementos de U
        for j in range(i, n):
            U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))    # U[i, j] = A[i, j] - sum(L[i, k] * U[k, j]) basicamente filas por columnas de la matriz A menos la suma de las filas por columnas de la matriz L por la matriz U
        
        # Calcular elementos de L
        for j in range(i + 1, n):
            L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]    # L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i])) / U[i, i] basicamente filas por columnas de la matriz A menos la suma de las filas por columnas de la matriz L por la matriz U dividido por la matriz U

    alert = "success"
    error_msg = "La factorización LU se realizó correctamente."
    return L, U, error_msg, alert

def jacobi(request):
    if request.POST:
        # Obtener los datos del formulario
        tol = request.POST.get('tol')
        columns = int(request.POST['columns'])
        rows = int(request.POST['rows'])
        A = np.zeros((rows, columns))
        
        for i in range(rows):
            for j in range(columns):
                A[i, j] = float(request.POST[f'A[{i}][{j}]'])
        
        b = np.zeros(rows)
        for i in range(rows):
            b[i] = float(request.POST[f'b[{i}]'])
        
        x0 = np.zeros(rows)
        for i in range(rows):
            x0[i] = float(request.POST[f'x0[{i}]'])
        
        x, iteraciones, error_msg, alert = metodo_jacobi(A, b, x0, tol, 100)
        
        
        
        return render(request, 'jacobi.html', {'x': x, 'img_url': 0, 'alert': alert, 'error_msg': error_msg, 'iteraciones': iteraciones, 'columns': columns, 'rows': rows})
    
    return render(request, 'jacobi.html')

def metodo_jacobi(A, b, x0, tol, max_iter):
    """
    Resuelve el sistema Ax = b utilizando el método de Jacobi.
    
    Parámetros:
        A: numpy.ndarray
            Matriz de coeficientes (cuadrada).
        b: numpy.ndarray
            Vector de términos independientes.
        x0: numpy.ndarray
            Vector inicial.
        tol: float
            Tolerancia para la convergencia.
        max_iter: int
            Número máximo de iteraciones.
            
    Retorna:
        x: numpy.ndarray
            Solución aproximada del sistema.
        iteraciones: int
            Número de iteraciones realizadas.
        error_msg: str
            Mensaje de error si ocurre algún problema.
        alert: str
            Tipo de alerta ('success' si todo va bien, 'danger' si hay error).
    """
    tol = float(tol)
    
    n, m = A.shape   # Obtener dimensiones de la matriz A
    error_msg = None
    alert = None
    
    if n != m:      # Verificar si la matriz es cuadrada
        error_msg = "Error: La matriz no es cuadrada."
        alert = "danger"
        return None, None, error_msg, alert
    
    if np.any(np.diag(A) == 0):     # Verificar si hay ceros en la diagonal principal
        error_msg = "Error: La matriz tiene ceros en la diagonal principal."
        alert = "danger"
        return None, None, error_msg, alert
    
    x = x0.copy()       # Copiar el vector inicial
    iteraciones = 0

    for k in range(max_iter):
        x_new = np.zeros_like(x)    # Crear un vector de ceros con la misma forma que x, es decir, n elementos para los valores del sistema de ecuaciones
        
        for i in range(n):    # Iterar sobre las filas de la matriz
            suma = sum(A[i, j] * x[j] for j in range(n) if j != i)    # Sumar los elementos de la fila actual, excepto el de la diagonal principal
            x_new[i] = (b[i] - suma) / A[i, i]      # Calcular el nuevo valor de la variable
        
        # Verificar criterio de convergencia
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:     # Calcular la norma infinito de la diferencia entre los vectores x_new y x, la norma infinito es el máximo valor absoluto de los elementos del vector, es decir el error máximo
            alert = "success"
            error_msg = "El sistema se resolvió correctamente."
            return x_new, iteraciones, error_msg, alert
        
        x = x_new
        iteraciones += 1
    
    error_msg = "Error: El método no converge después de {} iteraciones.".format(max_iter)
    alert = "danger"
    return None, iteraciones, error_msg, alert

def gauss_seidel(request):
    if request.POST:
        # Obtener los datos del formulario
        columns = int(request.POST['columns'])
        rows = int(request.POST['rows'])
        A = np.zeros((rows, columns))
        
        for i in range(rows):
            for j in range(columns):
                A[i, j] = float(request.POST[f'A[{i}][{j}]'])
        
        b = np.zeros(rows)
        for i in range(rows):
            b[i] = float(request.POST[f'b[{i}]'])
        
        x, etapas, error_msg, alert = gauss_seidel_method(A, b)
        
        ultima = etapas[-1]
        
        return render(request, 'gauss_seidel.html', {'x': x, 'img_url': 0, 'alert': alert, 'error_msg': error_msg, 'etapas': etapas, 'columns': columns, 'rows': rows, 'ultima': ultima})
    
    return render(request, 'gauss_seidel.html')