from django.shortcuts import render, redirect
from .models import *
import uuid  #gera id aleatorio


def homepage(request):
    banners = Banner.objects.filter(ativo=True)#aparecer banners ativos
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, nome_categoria=None):
  produtos = Produto.objects.filter(ativo=True) 
  if nome_categoria: 
    produtos = produtos.filter(categoria__nome=nome_categoria)
  context = {"produtos": produtos }
  return render(request, 'loja.html', context)


def ver_produto(request, id_produto, id_cor=None):
  tem_estoque = False
  cores = {}
  tamanhos = {}
  cor_selecionada = None
  if id_cor:
    cor_selecionada = Cor.objects.get(id=id_cor)
  produto = Produto.objects.get(id=id_produto)
  itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)  #v
  if len(itens_estoque) > 0:
    tem_estoque = True
    cores = {item.cor for item in itens_estoque}
    if id_cor:
        itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0, cor__id=id_cor)
        tamanhos = {item.tamanho for item in itens_estoque}  #filtra tam. disponivel
  context = {"produto": produto, "tem_estoque": tem_estoque, "cores": cores, "tamanhos": tamanhos, "cor_selecionada": cor_selecionada}
  return render(request, 'ver_produto.html', context)

#funcao de adicionar no carrinho
def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:  # se nao selecionar o tamanho
            return redirect('loja')  # redireciona para loja
        # pegar o cliente
        resposta = redirect('carrinho')  
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else: #se cliente nao estiver logado
            if request.COOKIES.get("id_sessao"):
               id_sessao = request.COOKIES.get("id_sessao")
            else:
               id_sessao = str(uuid.uuid4())
               resposta.set_cookie(key="id_sessao", value=id_sessao, max_age=60*60*24*30)
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao, )         
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)      
        # Adicionando prints para depuração
        print(f"Produto ID: {id_produto}, Tamanho: {tamanho}, Cor ID: {id_cor}")    
        try:
            item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        except ItemEstoque.DoesNotExist:
            print("ItemEstoque não encontrado")
            return redirect('loja')
        except ItemEstoque.MultipleObjectsReturned:
            print("Mais de um ItemEstoque encontrado")
            return redirect('loja')   
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save() 
        return resposta
    else:
        return redirect('loja')

def remover_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()
        tamanho = dados.get("tamanho")
        id_cor = dados.get("cor")
        if not tamanho:  # se nao selecionar o tamanho
            return redirect('loja')  # redireciona para loja
        # pegar o cliente
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:#se nao logado
             if request.COOKIES.get("id_sessao"):
           # Verifica se há um id_sessao nos cookies
              id_sessao = request.COOKIES.get("id_sessao")
         # Obtém ou cria um cliente com base no id_sessao
              cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
             else: #caso não tenha o id_sessao associado a ele
                return redirect('loja')
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)      
        # Adicionando prints para depuração
        print(f"Produto ID: {id_produto}, Tamanho: {tamanho}, Cor ID: {id_cor}")
       
        try:
            item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        except ItemEstoque.DoesNotExist:
            print("ItemEstoque não encontrado")
            return redirect('loja')
        except ItemEstoque.MultipleObjectsReturned:
            print("Mais de um ItemEstoque encontrado")
            return redirect('loja')
        
        try:
            item_pedido = ItensPedido.objects.get(item_estoque=item_estoque, pedido=pedido)
            item_pedido.quantidade -= 1
            if item_pedido.quantidade <= 0:
                item_pedido.delete()
            else:
                item_pedido.save()
        except ItensPedido.DoesNotExist:
            print("ItensPedido não encontrado")
        
        return redirect('carrinho')
    else:
        return redirect('loja')

def carrinho(request):
  if request.user.is_authenticated:  # Verifica se o usuário está autenticado
     # Se o cliente estiver autenticado, associa o cliente ao usuário
    cliente = request.user.cliente 
  else: #se cliente nao estiver autenticado
     if request.COOKIES.get("id_sessao"):
           # Verifica se há um id_sessao nos cookies
        id_sessao = request.COOKIES.get("id_sessao")
         # Obtém ou cria um cliente com base no id_sessao
        cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
     else: #caso não tenha o id_sessao associado a ele
        context = {"cliente_existente": False, "itens_pedido": None, "pedido": None}
          # Renderiza a página do carrinho com o contexto fornecido
        return render(request, 'carrinho.html', context)
  pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
  itens_pedido = ItensPedido.objects.filter(pedido=pedido)
  for item in itens_pedido:
    print(item.preco_total)
  context = {"itens_pedido": itens_pedido, "pedido": pedido, "cliente_existente": True}
  return render(request, 'carrinho.html', context)



def checkout(request):
   if request.user.is_authenticated: #Verif usuár autenticado
     # Se cliente autenticado, associa o cliente ao usuário
    cliente = request.user.cliente 
   else: #se nao estiver autenticado
     if request.COOKIES.get("id_sessao"):
           # Verifica se há um id_sessao nos cookies
        id_sessao = request.COOKIES.get("id_sessao")
         # Obtém ou cria um cliente com base no id_sessao
        cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
     else: #caso não tenha o id_sessao associado a ele
        return redirect("loja")
   pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
   enderecos = Endereco.objects.filter(cliente=cliente)
   context = {"pedido": pedido, "enderecos": enderecos}
   return render(request, 'checkout.html', context)


def adicionar_endereco(request):
    if request.method == "POST":
        # Tratar o envio do formulário
        if request.user.is_authenticated:# Verif usuário ta autenticado
            # Se cliente autenticado, associa o cliente ao usuário
            cliente = request.user.cliente
        else:  # Se não estiver autenticado
            if request.COOKIES.get("id_sessao"):
                # Verifica se há um id_sessao nos cookies
                id_sessao = request.COOKIES.get("id_sessao")
                # Obtém ou cria um cliente com base no id_sessao
                cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:  # Caso não tenha o id_sessao associado a ele
                return redirect("loja")
        dados = request.POST.dict()
        endereco = Endereco.objects.create(cliente=cliente, rua=dados.get("rua"), 
                                           numero=int(dados.get("numero")), estado=dados.get("estado"), 
                                           cidade=dados.get("cidade"), 
                                           cep=dados.get("cep"), 

                                           complemento=dados.get("complemento"))
        
        endereco.save()  #acabou de adicionar endereco
        return redirect("checkout")
    else:
        context = {}
        return render(request, "adicionar_endereco.html", context)
   

def minha_conta(request):
  return render(request, 'usuario/minha_conta.html')


def login(request):
  return render(request, 'usuario/login.html')


# TODO sempre que o usuario criar uma conta no nossso site, iremos criar uma cliente para ele.