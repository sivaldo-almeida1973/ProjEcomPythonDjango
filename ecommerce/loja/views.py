from django.shortcuts import render
from .models import *


def homepage(request):
    banners = Banner.objects.all()
    for banner in banners:
        print(banner.imagem)  # Verifique o caminho do arquivo
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request):
  produtos = Produto.objects.all() #pega todos os prod da tabela Produtos no bd
  context = {"produtos": produtos }
  return render(request, 'loja.html', context) #passa para html o contexto

def carrinho(request):
  return render(request, 'carrinho.html')


def checkout(request):
  return render(request, 'checkout.html')


def minha_conta(request):
  return render(request, 'usuario/minha_conta.html')


def login(request):
  return render(request, 'usuario/login.html')

