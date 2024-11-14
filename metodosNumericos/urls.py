"""
URL configuration for nombre_del_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from metodosNumericos import views as views
from Sistemas import views as SistemasViews
from Ecuaciones import views as EcuacionesViews
from Interpolacion import views as InterpolacionViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),  #home page
    path('ecuaciones/', EcuacionesViews.ecuaciones),  #ecuaciones page
    
    path('biseccion/', EcuacionesViews.biseccion),  #biseccion page
    path('biseccion/<str:error_msg>/<str:alert>/', EcuacionesViews.biseccion, name='biseccion'),  #biseccion page
    path('biseccion/result/<str:f>/<str:a>/<str:b>/<str:tol>/<int:n>/', EcuacionesViews.biseccion_result, name='biseccion_result'),     #biseccion result page
    
    path('regla_falsa/', EcuacionesViews.regla_falsa),  #regla falsa page
    path('regla_falsa/<str:error_msg>/<str:alert>/', EcuacionesViews.regla_falsa, name='regla_falsa'),  #regla falsa page
    path('regla_falsa/result/<str:f>/<str:a>/<str:b>/<str:tol>/<int:n>/', EcuacionesViews.regla_falsa_result, name='regla_falsa_result'),     #regla falsa result page
    
    path('punto_fijo/', EcuacionesViews.punto_fijo),  #punto fijo page
    path('punto_fijo/<str:error_msg>/<str:alert>/', EcuacionesViews.punto_fijo, name='punto_fijo'),  #punto fijo page
    path('punto_fijo/result/<str:g>/<str:x_origin>/<str:tol>/<int:n>/', EcuacionesViews.punto_fijo_result, name='punto_fijo_result'),     #punto fijo result page
    
    path('newton/', EcuacionesViews.newton),  #newton page
    path('newton/<str:error_msg>/<str:alert>/', EcuacionesViews.newton, name='newton'),  #newton page
    path('newton/result/<str:f>/<str:df>/<str:x_origin>/<str:tol>/<int:n>/', EcuacionesViews.newton_result, name='newton_result'),     #newton result page
    
    path('raices_multiples/', EcuacionesViews.raices_multiples),  #raices multiples page
    
    path('secante/', EcuacionesViews.secante),  #secante page
    
    path('sistemas/', SistemasViews.sistemas),  #sistemas page
]
