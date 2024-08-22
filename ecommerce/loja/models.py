from django.db import models
#importar a tabela do django
from django.contrib.auth.models import User

# Create your models here.
# bases de dados(tabelas)

class Cliente(models.Model):  #tabela Cliente
   nome = models.CharField(max_length=200, null=True, blank=True)
   email = models.CharField(max_length=200, null=True, blank=True)
   telefone = models.CharField(max_length=200, null=True, blank=True)
   id_sessao = models.CharField(max_length=200, null=True, blank=True) 
   usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # cada cliente so pode ter um uinico usuario e vice-versa


#(masculino, feminino, infantil...)
class Categoria(models.Model):
   nome = models.CharField(max_length=200, null=True, blank=True)

   def __str__(self):
       return str(self.nome) # faz aparecer o nome da categria no bd adm

#(Camisa, Camiseta, Bermuda, Calça...)
class Tipo(models.Model):
   nome = models.CharField(max_length=200, null=True, blank=True)

   def __str__(self):
       return str(self.nome) # faz aparecer o nome da categria no bd adm


class Produto(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True) 
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'Nome:{self.nome}, Categoria: {self.categoria}, Tipo: {self.tipo}, Preço: {self.preco}'



class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    cor =  models.CharField(max_length=200, null=True, blank=True)
    tamanho =  models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)


class Endereco(models.Model): 
    rua = models.CharField(max_length=200, null=True, blank=True)
    numero =  models.IntegerField(default=0)
    complemento = models.CharField(max_length=200, null=True, blank=True)
    cep = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, null=True, blank=True)
    estado = models.CharField(max_length=200, null=True, blank=True)
    cliente =  models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)


class Pedido(models.Model):
     cliente =  models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
     finalizado =  models.BooleanField(default=False)
     codigo_transacao =  models.CharField(max_length=200, null=True, blank=True)
     endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
     data_finalizacao = models.DateField(null=True, blank=True)


class ItensPedido(models.Model):
    itemes_toque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)

#sempre que criar um modelo(tabela) aqui , vai no admin registra-lo
class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino = models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    #definir um funcao str(como vai aparecer o texto no banner)
    def __str__(self) -> str:
        return f"{self.link_destino} = Ativo: {self.ativo}"





