# 3º passo
from django.urls import path, include
#importar tudo * do  arquivo views
from .views import *


urlpatterns = [
       # 1 link e qual views vai carregar esse link
    path('', homepage, name="homepage") ,#chama a funcao criada dentro views
    path('loja/', loja, name="loja"), #chama a funcao
    path('loja/<str:nome_categoria>/', loja, name="loja"), #link dinamico
    path('minhaconta/', minha_conta, name="minha_conta") ,
    path('login/', login, name="login"), #chama a funcao
    path('carrinho/', carrinho, name="carrinho") ,
    path('checkout/', checkout, name="checkout") ,

]
