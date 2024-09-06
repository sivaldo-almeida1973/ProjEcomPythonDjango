# 3º passo
from django.urls import path, include
#importar tudo * do  arquivo views
from .views import *


urlpatterns = [
       # link ==funcao == name é a url que vai ser usada no html 
    path('', homepage, name="homepage") ,#chama a funcao criada dentro views
    path('loja/', loja, name="loja"), #chama a funcao  link loja
    path('loja/<str:filtro>/', loja, name="loja"), #link dinamico loja
    path('produto/<int:id_produto>/', ver_produto, name="ver_produto"),
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),
    path('carrinho/', carrinho, name="carrinho") ,
    path('checkout/', checkout, name="checkout") ,
    path('adicionarcarrinho/<int:id_produto>/', adicionar_carrinho, name="adicionar_carrinho"),
    path('removercarrinho/<int:id_produto>/', remover_carrinho, name="remover_carrinho"),
    path('adicionarendereco/', adicionar_endereco, name="adicionar_endereco"),

    path('minhaconta/', minha_conta, name="minha_conta") ,
    path('login/', login, name="login"), 
    path('criarconta/', criar_conta, name="criar_conta"), 

]
