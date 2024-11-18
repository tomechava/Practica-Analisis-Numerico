# Proyecto de Análisis Numérico

## Descripción
Este proyecto es una herramienta numérica autocontenida desarrollada para la materia de **Análisis Numérico**. La herramienta implementa diversos métodos numéricos para la resolución de ecuaciones de una variable, sistemas de ecuaciones y métodos de interpolación. El objetivo es ofrecer una plataforma intuitiva y funcional que permita visualizar el comportamiento de los métodos y analizar los errores asociados a cada uno de ellos.

La aplicación está desarrollada en Django y está diseñada para facilitar el aprendizaje y la aplicación de métodos numéricos en un entorno web.

## Características
- **Evaluador de funciones**: Permite al usuario ingresar funciones matemáticas para evaluar.
- **Métodos de ecuaciones de una variable**:
  - Búsquedas incrementales
  - Método de Bisección
  - Regla Falsa
  - Método de Punto Fijo
  - Método de Newton
  - Raíces Múltiples
  - Método de la Secante
- **Métodos de sistemas de ecuaciones**:
  - Eliminación Gaussiana
  - Gauss con pivoteo parcial
  - Factorización LU (opciones: Cholesky, Doolittle, o Crout)
  - Método de Jacobi
  - Método de Gauss-Seidel
- **Métodos de interpolación** (especificar los métodos si los tienes definidos)
- **Visualización de errores**: Graficador que permite elegir entre error absoluto y relativo para visualizar la convergencia y el comportamiento de los métodos.

## Requisitos
- Python 3.x
- Django
- [Otros requisitos adicionales si aplican, por ejemplo, NumPy o Matplotlib]

Para instalar las dependencias:
```bash
pip install -r requirements.txt
```

# **Manual de Usuario**

Este manual tiene como objetivo guiar al usuario en el uso correcto de la aplicación para resolver **sistemas de ecuaciones** y **ecuaciones de una variable**. Se incluye la descripción de los campos necesarios en los formularios, las restricciones y el formato aceptado para evitar errores.

---

## **Campos Generales del Formulario**

### **1. Formato de Funciones**
- Todas las funciones deben ingresarse en formato compatible con Python:
  - Potencias: Utilizar `**` en lugar de `^`.
    - **Correcto:** `x**2 - 4*x + 4`
    - **Incorrecto:** `x^2 - 4x + 4`
  - Multiplicaciones: Siempre explícitas.
    - **Correcto:** `2*x`
    - **Incorrecto:** `2x`
  - Funciones matemáticas admitidas:
    - `math.sin(x)`, `math.cos(x)`, `math.exp(x)`, etc.
  - La variable independiente debe ser `x`.

### **2. Tolerancia (`tol`)**
- Valor decimal positivo que define la precisión deseada.
  - **Ejemplo:** `0.001`

### **3. Máximo de Iteraciones (`max_iter`)**
- Número entero positivo que establece el límite de iteraciones.
  - **Ejemplo:** `100`

---

## **Resolución de Ecuaciones de Una Variable**

### **Campos Específicos**
- **Ecuación (`f(x)`):**
  - Ingresar una función continua en formato Python.
  - Ejemplo:
    ```python
    f(x) = x**2 - 4
    ```

- **Derivada (`f'(x)`):** *(Requerido solo para Newton-Raphson)*
  - No ingresar la derivada de la funcion, esta será calculada por el metodo automaticamente.

- **Punto Inicial (`x0`):**
  - Valor numérico real para iniciar el método.
  - Ejemplo:
    ```python
    x0 = 1
    ```

- **Intervalo (`a, b`):** *(Requerido solo para Regla Falsa)*
  - Especificar un intervalo que contenga una raíz, es decir, \(f(a) \cdot f(b) < 0\).
  - Ejemplo:
    ```python
    a = 0, b = 2
    ```

### **Caso de Uso**
1. Ingrese la ecuación:
f(x) = x**2 - 4

2. Seleccione el método deseado (por ejemplo, **Newton-Raphson**).
3. Proporcione los campos requeridos:
- Derivada: `f'(x) = 2*x`
- Punto inicial: `x0 = 1`
- Tolerancia: `0.001`
- Máximo de iteraciones: `100`
4. Presione **Calcular**. La solución y la gráfica del proceso iterativo se mostrarán.

---

## **Resolución de Sistemas de Ecuaciones**

### **Campos Específicos**
- **Matriz de Coeficientes (`A`):**
- Debe ser cuadrada y no contener ceros en la diagonal principal.
- Ejemplo:
 ```python
 A = [[4, -1, 0],
      [-1, 4, -1],
      [0, -1, 4]]
 ```

- **Vector Independiente (`b`):**
- Debe tener el mismo número de elementos que las filas de la matriz `A`.
- Ejemplo:
 ```python
 b = [15, 10, 10]
 ```

- **Vector Inicial (`x0`):**
- Ingrese una estimación inicial.
- Ejemplo:
 ```python
 x0 = [0, 0, 0]
 ```

### **Caso de Uso**
1. Ingrese la matriz y el vector independiente:
```python
A = [[4, -1, 0],
     [-1, 4, -1],
     [0, -1, 4]]

b = [15, 10, 10]
```
2. Seleccione el método deseado (por ejemplo, Jacobi).
3. Proporcione los campos requeridos:
  - Vector inicial: x0 = [0, 0, 0]
  - Tolerancia: 0.001
  - Máximo de iteraciones: 50
4. Presione Calcular. La solución y la gráfica de convergencia se mostrarán.

## Notas Finales
Si tiene dudas sobre el formato de los campos, revise los ejemplos provistos o consulte la documentación de Python.
Las gráficas generadas durante el proceso pueden visualizarse y descargarse desde la interfaz web.
En caso de errores persistentes, contacte al desarrollador.
