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
