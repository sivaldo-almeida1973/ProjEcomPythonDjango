from django.shortcuts import render, redirect
from .models import *
import uuid  #gera id aleatorio
from .utils import filtra_produtos, preco_minimo_maximo, ordenar_produtos
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime



def homepage(request):
    banners = Banner.objects.filter(ativo=True)#aparecer banners ativos
    context = {"banners": banners}
    return render(request, 'homepage.html', context)


def loja(request, filtro=None):
    produtos = Produto.objects.filter(ativo=True) 
    produtos = filtra_produtos(produtos, filtro)
    #aplicar filtros do formulario(filtro de preco)
    if request.method == "POST":
       dados = request.POST.dict()
       produtos = produtos.filter(preco__gte=dados.get("preco_minimo"), preco__lte=dados.get("preco_maximo"))
       if "tamanho" in dados:
          itens = ItemEstoque.objects.filter(produto__in=produtos, tamanho=dados.get("tamanho"))
          ids_produtos = itens.values_list("produto", flat=True).distinct()
          produtos = produtos.filter(id__in=ids_produtos)
       if "tipo" in dados:
          produtos = produtos.filter(tipo__slug=dados.get("tipo"))
       if "categoria" in dados:
          produtos = produtos.filter(categoria__slug=dados.get("categoria"))
           
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list("tamanho", flat=True).distinct()
    ids_categorias = produtos.values_list("categoria", flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=ids_categorias)
    ids_cores = itens.values_list("cor", flat=True).distinct()
    cores = Cor.objects.filter(id__in=ids_cores)
    minimo, maximo = preco_minimo_maximo(produtos)

     #caso não encotre o parametro ordem, uso como parametro menor-preco
    ordem = request.GET.get("ordem", "menor-preco")
    #produtos vai ser a minha funcao ordenar_produtos (utils.py)
    produtos = ordenar_produtos(produtos, ordem)

    context = {
        "produtos": produtos,
        "minimo": minimo,
        "maximo": maximo,
        "tamanhos": tamanhos,
        "cores": cores,
        "categorias": categorias
    }
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
   context = {"pedido": pedido, "enderecos": enderecos, "erro": None}
   return render(request, 'checkout.html', context)


def finalizar_pedido(request, id_pedido):
   if request.method == "POST":
      erro = None
      dados = request.POST.dict()

      total = dados.get("total")
      pedido = Pedido.objects.get(id=id_pedido)

      if total != pedido.preco_total:
         erro = "preco"
      #verificar se ta vindo um endereco
      if not "endereco" in dados:
         erro = "endereco"
      else:
         endereco = dados.get("endereco")
         pedido.endereco = endereco

      if not request.user.is_authenticated:
         email = dados.get("email")
         try:
            validate_email(email)
         except ValidationError:
            erro = "email"
         if not erro:
            clientes = Cliente.objects.filter(email=email)
            if clientes:
               pedido.cliente = clientes[0]
            else:
               pedido.cliente.email = email
               pedido.cliente.save()
      codigo_transacao = f"{pedido.id}-{datetime.now().timestamp()}"
      pedido.codigo_transacao = codigo_transacao
      pedido.save()          
      if erro:# tratar se der algum erro acima
         enderecos = Endereco.objects.filter(cliente=pedido.cliente)
         context = {"erro": erro, "pedido": pedido, "enderecos": enderecos}
         return render(request, "checkout.html", context)
      else:
         # Todo pagamento do usuario
         return redirect("checkout")
   else:
      return redirect("loja")



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


@login_required  #so acessa que estiver logado
def minha_conta(request):
  erro = None
  alterado = False
  if request.method == 'POST':
     dados = request.POST.dict()
     print(dados)
     if "senha_atual" in dados:
        #alteracao de senha
        senha_atual = dados.get("senha_atual")
        nova_senha = dados.get("nova_senha")
        nova_senha_confirmacao = dados.get("nova_senha_confirmacao")
        if nova_senha == nova_senha_confirmacao:  #verificar se a senha atual esta certa
          #autentica usuario
           usuario = authenticate(request, username=request.user.email, password=senha_atual)
           if usuario: #se usuario existir
              #senha correta
              usuario.set_password(nova_senha)
              usuario.save()
              alterado = True
           else:
              erro = "senha_incorreta"
        else:
           erro = "senhas_diferentes"
           #alterar email
     elif "email" in dados:
        email = dados.get("email")
        telefone = dados.get("telefone")
        nome = dados.get("nome")   
        #se ele ta tentado modificar o email dele
        if email != request.user.email:
           #vou procurar se tem algum usuario com email == ao novo email dele 
           usuarios = User.objects.filter(email=email)
           if len(usuarios) > 0:
              erro = "email_existente"
        if not erro: #se nao deu erro
           #confirmar modificar email
           cliente = request.user.cliente
           cliente.email = email
           request.user.email = email
           request.user.email = email
           cliente.nome = nome
           cliente.telefone = telefone
           cliente.save()
           request.user.save()
           alterado = True

     else:
        erro = "formulario_invalido"
  context = {"erro": erro, "alterado": alterado}
  return render(request, 'usuario/minha_conta.html', context)


@login_required  #so acessa que estiver logado
def meus_pedidos(request):
   cliente = request.user.cliente
   pedidos = Pedido.objects.filter(finalizado=True, cliente=cliente).order_by("-data_finalizacao")
   context = {"pedidos": pedidos}
   return render(request, "usuario/meus_pedidos.html", context)



def fazer_login(request):
  erro = False
  #se usuario estiver autenticado
  if request.user.is_authenticated:
     #redireciona para loja
     return redirect('loja')
  #se nao estiver logado
  if request.method == 'POST':
     dados = request.POST.dict()#pega os dados que estao vindo do form
     if "email" in dados and "senha" in dados:
        email = dados.get("email")
        senha = dados.get("senha")
        usuario = authenticate(request, username=email, password=senha)
        #fazer login se encontrar usuario
        if usuario:
            login(request, usuario)
            return redirect('loja')
        else: #caso nao encontre o usuario
            erro = True
     else:
        erro = True
  context = {"erro": erro}
  return render(request, 'usuario/login.html', context) #carrega tela login


def criar_conta(request):
  erro = None
  if request.user.is_authenticated:
     return redirect("loja")
  if request.method == 'POST':
      dados = request.POST.dict()
      if "email" in dados and "senha" in dados and "confirmacao_senha" in dados:
       #criar conta
        email = dados.get("email")
        senha = dados.get("senha")
        confirmacao_senha = dados.get("confirmacao_senha")
        try:
           validate_email(email)
        except ValidationError:
           erro = "email_inválido"
        if senha == confirmacao_senha:
           #criar conta
           usuario, criado = User.objects.get_or_create(username=email, email=email)
           if not criado:
              erro = "usuario_existente"
           else:
              usuario.set_password(senha)
              usuario.save()
               #fazer login do usuario
              usuario = authenticate(request, username=email, password=senha)
              login(request, usuario)
              #verificar se existe o id_sessao nos cookies
              if request.COOKIES.get("id_sessao"):
                 # Verifica se há um id_sessao nos cookies
                 id_sessao = request.COOKIES.get("id_sessao")
                 # Obtém ou cria um cliente com base no id_sessao
                 cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
              else:
                 cliente, criado = Cliente.objects.get_or_create(email=email)
              cliente.usuario = usuario
              cliente.email = email       
              cliente.save()
              return redirect("loja")
        else:
           erro = "senhas_diferentes"
      else:
        erro = "preenchimento"
  context = {"erro": erro}
  return render(request, 'usuario/criar_conta.html', context)

@login_required  #so acessa que estiver logado
def fazer_logout(request):
   logout(request)
   return redirect("fazer_login")
   
   
   


