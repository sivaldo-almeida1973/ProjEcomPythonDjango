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


def ver_produto(request, id_produto, id_cor=None):
  tem_estoque = False
  cores = {}
  tamanhos = {}
  nome_cor_selecionada = None
  if id_cor:
    cor = Cor.objects.get(id=id_cor)
    nome_cor_selecionada = cor.nome
  produto = Produto.objects.get(id=id_produto)
  itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)  #v
  if len(itens_estoque) > 0:
    tem_estoque = True
    cores = {item.cor for item in itens_estoque}
    if id_cor:
        itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id=id_cor)
        tamanhos = {item.tamanho for item in itens_estoque}  #filtra tam. disponivel
  context = {"produto": produto, "itens_estoque": itens_estoque, "tem_estoque": tem_estoque, "cores": cores, "tamanhos": tamanhos, 'nome_cor_selecionada': nome_cor_selecionada}
  return render(request, 'ver_produto.html', context)


def carrinho(request):
  return render(request, 'carrinho.html')


def checkout(request):
  return render(request, 'checkout.html')


def minha_conta(request):
  return render(request, 'usuario/minha_conta.html')


def login(request):
  return render(request, 'usuario/login.html')

