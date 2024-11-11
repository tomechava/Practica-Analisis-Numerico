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
    path('sistemas/', SistemasViews.sistemas),  #sistemas page
    path('ecuaciones/', EcuacionesViews.ecuaciones),  #ecuaciones page
    path('interpolacion/', InterpolacionViews.interpolacion),  #interpolacion page
]
