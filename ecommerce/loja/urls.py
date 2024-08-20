# 3º passo
from django.urls import path, include
#importar tudo * do  arquivo views
from .views import *


urlpatterns = [

    path('', homepage, name="homepage") # chama a funcao que foi criada dentro do views

    

]
