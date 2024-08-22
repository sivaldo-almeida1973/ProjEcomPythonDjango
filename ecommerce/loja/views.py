from django.shortcuts import render
from .models import *


def homepage(request):
    banners = Banner.objects.filter(ativo=True)#aparecer banners ativos
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, nome_categoria=None):
  produtos = Produto.objects.filter(ativo=True) #prod da tabela Prod no bd
  if nome_categoria: #se tiver nome da categoria
    produtos = produtos.filter(categoria__nome=nome_categoria)# faz isso
  context = {"produtos": produtos }
  return render(request, 'loja.html', context) #passa para html o contexto

def ver_produto(request, id_produto):
  produto = Produto.objects.get(id=id_produto)
  itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)  #valor maior que (quantidade__gt=0)
  context = {"produto": produto, "itens_estoque": itens_estoque}
  return render(request, 'ver_produto.html', context)


def carrinho(request):
  return render(request, 'carrinho.html')


def checkout(request):
  return render(request, 'checkout.html')


def minha_conta(request):
  return render(request, 'usuario/minha_conta.html')


def login(request):
  return render(request, 'usuario/login.html')

