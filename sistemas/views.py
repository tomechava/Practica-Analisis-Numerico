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
