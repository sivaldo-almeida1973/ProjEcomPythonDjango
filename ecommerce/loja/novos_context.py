from .models import Pedido, ItensPedido, Cliente, Categoria, Tipo

#logica de adicionar itens no carrinho
def carrinho(request):
  quantidade_produtos_carrinho = 0
  if request.user.is_authenticated:
    cliente = request.user.cliente
  else: #se cliente nao estiver logado
     if request.COOKIES.get("id_sessao"):
           # Verifica se há um id_sessao nos cookies
        id_sessao = request.COOKIES.get("id_sessao")
         # Obtém ou cria um cliente com base no id_sessao
        cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
     else: #caso não tenha o id_sessao associado a ele
        return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}
  pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
  #quantos produtos tem no pedido do usuario
  itens_pedido = ItensPedido.objects.filter(pedido=pedido)
  for item in itens_pedido:
    quantidade_produtos_carrinho += item.quantidade
  return {"quantidade_produtos_carrinho": quantidade_produtos_carrinho}


def categorias_tipos(request):
   categorias_navegacao = Categoria.objects.all()
   tipos_navegacao = Tipo.objects.all()
   return {"categorias_navegacao": categorias_navegacao, "tipos_navegacao": tipos_navegacao}