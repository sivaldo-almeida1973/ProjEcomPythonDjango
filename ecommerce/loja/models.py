from django.db import models
#importar a tabela do django
from django.contrib.auth.models import User

# Create your models here.
# bases de dados(tabelas)

class Cliente():
   nome = models.CharField(max_length=200, null=True, blank=True)
   email = models.CharField(max_length=200, null=True, blank=True)
   telefone = models.CharField(max_length=200, null=True, blank=True)
   id_sessao = models.CharField(max_length=200, null=True, blank=True) 
   usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # cada cliente so pode ter um uinico usuario e vice-versa

#Produto
   # imagem
   # nome
   # preco
   # ativo
   #categoria
   # tipo



# Categorias
    #nome


# Tipos 
    #nome


# ItemEstoque
    # produto(ex: camisa)
    # cor(ex: azul, laranja, verde)
    # tamanho (ex: P, M, G)
    # quantidade



# ItensPedido
    # itemestoque
    # quantidade


#Pedido
    # cliente
    # data_finalizacao
    # finalizado
    # id_transacao
    # endereco
    # itenspedido

#Endereco 
    # rua
    # numero
    # complemento
    # cep
    # cidade
    # estado
    # cliente



